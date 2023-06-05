import email
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from workout_tracker.models import Exercise, Workout
from workout_tracker.serializers import ExerciseSerializer, WorkoutSerializer

User = get_user_model()

class ExerciseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.trainer_user = User.objects.create_user(
            username='trainer', 
            password='testpass',
            is_trainer=True,
            email = 'test@gmail.com'
        )
        self.client.force_authenticate(user=self.trainer_user)
        self.exercise_data = {'name': 'Squats','description': 'test'}
        self.exercise = Exercise.objects.create(name='Push-ups', description = 'test')

    def test_list_exercises(self):
        response = self.client.get(reverse('exercise-list'))
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_exercise(self):
        response = self.client.post(reverse('exercise-create'), data=self.exercise_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 2)
        self.assertEqual(Exercise.objects.last().name, self.exercise_data['name'])

    def test_retrieve_exercise(self):
        response = self.client.get(reverse('exercise-detail', args=[self.exercise.id]))
        serializer = ExerciseSerializer(self.exercise)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_exercise(self):
        updated_data = {'name': 'Pull-ups', 'description' : ' test 2'}
        response = self.client.put(reverse('exercise-detail', args=[self.exercise.id]), data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Exercise.objects.get(id=self.exercise.id).name, updated_data['name'])

    def test_delete_exercise(self):
        response = self.client.delete(reverse('exercise-detail', args=[self.exercise.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.count(), 0)
