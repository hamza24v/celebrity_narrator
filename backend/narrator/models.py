from django.db import models

class Narration(models.Model):
    image = models.ImageField(upload_to='images/')
    analysis = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
