from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from rest_framework import status
from rest_framework.test import APIClient

from workout_tracker.models import Exercise, Workout
from workout_tracker.serializers import ExerciseSerializer, WorkoutSerializer
from django.contrib.auth import get_user_model

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


class WorkoutListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email = "test@gmai.com",

        )
        self.trainer = User.objects.create_user(
            username='traineruser',
            password='trainerpass',
            email = "test2@gmai.com",
            is_trainer=True
        )
        self.workout1 = Workout.objects.create(
            name='Workout1',
            description='Test Description',
        )
        self.workout2 = Workout.objects.create(
            name='Workout2',
            description='Test Description 2',
        )
        self.url = reverse('workout-list')

    def test_get_workouts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Workout1')
        self.assertEqual(response.data[1]['name'], 'Workout2')


class WorkoutDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email = "test@gmai.com",

        )
        self.trainer = User.objects.create_user(
            username='traineruser',
            password='trainerpass',
            email = "test2@gmai.com",
            is_trainer=True

        )
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test Description',
        )
        self.url = reverse('workout-detail', args=[self.workout.id])

    def test_get_workout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Workout')

    def test_update_workout_not_trainer(self):
        data = {
            'name': 'Updated Workout',
            'description': 'Updated Description',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_workout_trainer(self):
        data = {
            'name': 'Updated Workout',
            'description': 'Updated Description',
        }
        self.client.force_authenticate(user=self.trainer)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Workout')

    def test_delete_workout_not_trainer(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_workout_trainer(self):
        self.client.force_authenticate(user=self.trainer)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Workout.objects.count(), 0)

class UserWorkoutsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass',
            username='testuser'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout'
        )
        self.user.workouts.add(self.workout)

    def test_user_workouts_view(self):
        url = reverse('user-workouts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Workout')