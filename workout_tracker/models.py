from django.db import models

# Create your models here.

from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='exercise_images/', blank=True, null=True)
    video = models.FileField(upload_to='exercise_videos/', blank=True, null=True)

    def __str__(self):
        return self.name