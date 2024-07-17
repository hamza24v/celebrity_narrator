from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
from .models import Narration
from .serializers import NarrationSerializer
from openai import OpenAI
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import base64
import os  
import time

load_dotenv()

eleven_lab_client = ElevenLabs(
    api_key = os.getenv("ELEVENLABS_API_KEY")
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
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
        audio = eleven_lab_client.text_to_speech(
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
        retry_attempts = 3
        for attempt in range(retry_attempts):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": """
                            You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                            Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                            """,
                        },
                    ]
                    + script,
                    max_tokens=500,
                )
                response_text = response.choices[0].message['content']
                return response_text
            except client.chat.error.RateLimitError as e:
                if attempt < retry_attempts - 1:
                    print(f"Rate limit exceeded, retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise


    @action(detail=True, methods=['post'])
    def process_image(self, request, pk=None):
        print("Request Data:", request.data)
        narration = self.get_object()
        image_path = narration.image.path

        
        base64_image = self.encode_image(image_path)
        print("Base64 Image:", base64_image[:100])
        
        script = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"},
                ],
            },
        ]

        analysis = self.analyze_image(base64_image, script=script)
        print("Analysis:", analysis)

        narration.analysis = analysis # Save analysis to model
        narration.save()

        # Generate and save audio file
        audio_file_path = self.play_audio(analysis)
        with open(audio_file_path, "rb") as f:
            narration.audio_file.save(os.path.basename(audio_file_path), ContentFile(f.read()))
        
        print("Audio File URL:", narration.audio_file.url)
        return Response({'status': 'processed', 'analysis': analysis, 'audio_file': narration.audio_file.url})
