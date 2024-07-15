from django.db import models

class Narration(models.Model):
    image = models.ImageField(upload_to='images/')
    analysis = models.TextField()
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
