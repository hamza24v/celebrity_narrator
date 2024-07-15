from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
from .models import Narration
from .serializers import NarrationSerializer
import openai
from elevenlabs.client import ElevenLabs
import base64
import os
import time


openai.api_key = os.getenv("OPENAI_API_KEY")
client = ElevenLabs(
    api_key = os.getenv("ELEVENLABS_API_KEY")
)

class NarrationViewSet(viewsets.ModelViewSet):
    queryset = Narration.objects.all()
    serializer_class = NarrationSerializer
    parser_classes = (MultiPartParser, FormParser)

    def encode_image(self, image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    raise
                time.sleep(0.1)

    def play_audio(self, text):
        audio = client.text_to_speech(
            text=text,
            voice=os.getenv("ELEVENLABS_VOICE_ID"),
            model="eleven_monolingual_v1",
            voice_settings={
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        )
        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.mp3")
        with open(file_path, "wb") as f:
            f.write(audio)
        return file_path

    def analyze_image(self, base64_image, script):
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                    Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                    """,
                },
            ]
            + script
            + [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image"},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"},
                    ],
                },
            ],
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        return response_text

    @action(detail=True, methods=['post'])
    def process_image(self, request, pk=None):
        narration = self.get_object()
        image_path = narration.image.path

        
        base64_image = self.encode_image(image_path)

        
        script = []

        analysis = self.analyze_image(base64_image, script=script)

        narration.analysis = analysis # Save analysis to model
        narration.save()

        # Generate and save audio file
        audio_file_path = self.play_audio(analysis)
        with open(audio_file_path, "rb") as f:
            narration.audio_file.save(os.path.basename(audio_file_path), ContentFile(f.read()))

        return Response({'status': 'processed', 'analysis': analysis, 'audio_file': narration.audio_file.url})
