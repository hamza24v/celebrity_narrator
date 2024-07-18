import errno, os, time, uuid, openai, tiktoken, io, base64, threading
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.urls import reverse
from .models import Narration
from .serializers import NarrationSerializer
from openai import OpenAI
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from PIL import Image

load_dotenv()

eleven_lab_client = ElevenLabs(
    api_key = os.getenv("ELEVENLABS_API_KEY")
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# used to delete image and audio file path after client recieves and plays narration
# So rest assured if you're concerned about face pic being stored 
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

class NarrationViewSet(viewsets.ModelViewSet):
    queryset = Narration.objects.all()
    serializer_class = NarrationSerializer
    parser_classes = (MultiPartParser, FormParser)

    def encode_image(self, image_path, quality=50):
        try:
            with Image.open(image_path) as image_file:
                image_file = image_file.convert("RGB")
                buffer = io.BytesIO()
                image_file.save(buffer, format="JPEG", quality=quality)
                base64_image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
                return {'success': True, 'image': base64_image_data}
        except IOError as e:
            if e.errno != errno.EACCES:
                return {"success": False, "message": str(e)}
            time.sleep(0.1)

    def play_audio(self, text, request):
        try:
            audio = eleven_lab_client.text_to_speech.convert(
                text=text,
                voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
                model_id="eleven_monolingual_v1",
                voice_settings={
                    "stability": 0.5,
                    "similarity_boost": 0.75
                },
            )

            # creating mp3 file and storing in dir
            file_name = f"{uuid.uuid4()}.mp3" # generates unique output file name
            file_path = os.path.join(settings.MEDIA_ROOT, "audio", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # writing audio to file
            with open(file_path, "wb") as f:
               for chunk in audio:
                    if chunk:
                        f.write(chunk)

            audio_url = request.build_absolute_uri(f'{settings.MEDIA_URL}audio/{file_name}')

            threading.Timer(30.0, delete_file, [file_path]).start()  # deletes audio after 30 seconds

            return {'success': True, 'audio_url': audio_url}
        except Exception as err:
            error = {"success": False, "errorFrom": "Eleven labs API", 'message': str(err)}
            return error

        

    def analyze_image(self, base64_image):
        try:
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Sir David Attenborough. Narrate the person in the image as if it is a nature documentary.
                    Make it snarky, funny and short. Don't repeat yourself. If I do anything remotely interesting, make a big deal about it!
                    """,
                },
                {
                    "role": "user",
                    "content": f"Describe the following person in detail: data:image/jpeg;base64,{base64_image}"
                }
            ]
            token_count = sum(len(encoding.encode(message['content'])) for message in messages) # counts number of tokens
            print(f"Token count: {token_count}")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=700,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            return {"success": True, 'content': response.choices[0].message.content}
        except openai.APIError as err:
            error = {"success": False, "errorFrom": "Openai API", 'message': str(err)}
            return error 


    @action(detail=True, methods=['post'])
    def process_image(self, request, pk=None):
        narration = self.get_object()
        image_path = narration.image.path

        # encoding image
        base64_image = self.encode_image(image_path, quality=65)
        if not base64_image['success']:
            return Response(base64_image, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Encoded Image status: Success")

        # analyzing image
        analysis = self.analyze_image(base64_image['image'])
        if not analysis['success']:
            return Response(analysis, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Analysis status: Success")
        narration.analysis = analysis['content']  # saving analysis to model
        narration.save()

        print("Analysis: ", analysis)
        # generating and saving audio file
        audio = self.play_audio(analysis['content'], request)
        if audio['success']:
            audio_url = audio['audio_url']
        else:
            return Response(audio, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Audio file url: ", audio_url)
        threading.Timer(30.0, delete_file, [image_path]).start()  # deletes image after 30 seconds

        return Response({'status': 'processed', 'analysis': analysis['content'], 'audio_file': audio_url})

