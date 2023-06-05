from django.db import models
from django.conf import settings
from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='exercise_images/', blank=True, null=True)
    video = models.FileField(upload_to='exercise_videos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name

class AccountWorkout(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('account', 'workout')