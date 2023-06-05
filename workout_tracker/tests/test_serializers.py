from django.test import TestCase
from workout_tracker.models import Exercise, Workout
from rest_framework import serializers
from ..serializers import WorkoutSerializer, ExerciseSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
import base64

class ExerciseSerializerTest(TestCase):
    
    def setUp(self):
        self.exercise = Exercise.objects.create(name='push-up', description='A classic bodyweight exercise', image='push-up.jpg', video='test.mp4')
    
    def test_serializer(self):
        serializer = ExerciseSerializer(instance=self.exercise)
        expected_data = {
        'name': 'push-up', 
        'description':'A classic bodyweight exercise', 
        'image': '/media/push-up.jpg', 
        'video': '/media/test.mp4'}

        self.assertEqual(serializer.data, expected_data)


class WorkoutSerializerTest(TestCase):
    
    def setUp(self):
        self.exercise1 = Exercise.objects.create(name='push-up', description='A classic bodyweight exercise', image='push-up.jpg', video='test3.mp4')
        self.exercise2 = Exercise.objects.create(name='squat', description='A fundamental lower body exercise', image='squat.jpg', video='test4.mp4')
        self.workout = Workout.objects.create(name='upper body workout', description='A workout for the upper body')
        self.workout.exercises.set([self.exercise1, self.exercise2])
    
    
    def test_create(self):


        input_data = {
            'name': 'full body workout',
            'description': 'A workout for the whole body',
            'exercises': [
                {
                    'name': 'push-up',
                    'description': 'A classic bodyweight exercise',
                    'image':  SimpleUploadedFile('test_image.jpg', b'content'),
                    'video': SimpleUploadedFile('test_video.mp4', b'content'),
                },
                {
                    'name': 'squat',
                    'description': 'A fundamental lower body exercise',
                    'image':  SimpleUploadedFile('test_image.jpg', b'content'),
                    'video': SimpleUploadedFile('test_video.mp4', b'content'),
                }
            ]
        }
        serializer = WorkoutSerializer(data=input_data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())
        workout = serializer.save()
        self.assertEqual(workout.name, 'full body workout')
        self.assertEqual(workout.description, 'A workout for the whole body')
        self.assertEqual(workout.exercises.count(),2)