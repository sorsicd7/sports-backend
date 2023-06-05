from django.test import TestCase
from workout_tracker.models import Exercise, Workout, AccountWorkout
from django.contrib.auth import get_user_model

User = get_user_model()

class ExerciseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Exercise.objects.create(name='Push-ups', description='Do 20 push-ups')

    def test_name_label(self):
        exercise = Exercise.objects.get(id=1)
        field_label = exercise._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        exercise = Exercise.objects.get(id=1)
        field_label = exercise._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_image_label(self):
        exercise = Exercise.objects.get(id=1)
        field_label = exercise._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_video_label(self):
        exercise = Exercise.objects.get(id=1)
        field_label = exercise._meta.get_field('video').verbose_name
        self.assertEqual(field_label, 'video')

    def test_name_max_length(self):
        exercise = Exercise.objects.get(id=1)
        max_length = exercise._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_image_upload_to(self):
        exercise = Exercise.objects.get(id=1)
        upload_to = exercise._meta.get_field('image').upload_to
        self.assertEqual(upload_to, 'exercise_images/')

    def test_video_upload_to(self):
        exercise = Exercise.objects.get(id=1)
        upload_to = exercise._meta.get_field('video').upload_to
        self.assertEqual(upload_to, 'exercise_videos/')

    def test_object_name_is_name(self):
        exercise = Exercise.objects.get(id=1)
        expected_object_name = exercise.name
        self.assertEqual(expected_object_name, str(exercise))



class WorkoutModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.exercise = Exercise.objects.create(name='Push-ups', description='Do 20 push-ups')
        cls.workout = Workout.objects.create(name='Full-body workout', description='Do 3 sets of 10 reps for each exercise')
        cls.workout.exercises.add(cls.exercise)

    def test_name_label(self):
        workout = Workout.objects.get(id=self.workout.id)
        field_label = workout._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        workout = Workout.objects.get(id=self.workout.id)
        field_label = workout._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_exercises_label(self):
        workout = Workout.objects.get(id=self.workout.id)
        field_label = workout._meta.get_field('exercises').verbose_name
        self.assertEqual(field_label, 'exercises')

    def test_name_max_length(self):
        workout = Workout.objects.get(id=self.workout.id)
        max_length = workout._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        workout = Workout.objects.get(id=self.workout.id)
        expected_object_name = workout.name
        self.assertEqual(expected_object_name, str(workout))

    def test_exercises_count(self):
        workout = Workout.objects.get(id=self.workout.id)
        exercise_count = workout.exercises.count()
        self.assertEqual(exercise_count, 1)

    def test_exercises_through(self):
        workout = Workout.objects.get(id=self.workout.id)
        exercise = Exercise.objects.get(id =self.exercise.id)
        through = workout.exercises.through
        self.assertTrue(through.objects.filter(workout=workout, exercise=exercise).exists())


class AccountWorkoutTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='test@gmail.com')
        self.user2 = User.objects.create(username='user2',email='test2@gmail.com')
        self.workout1 = Workout.objects.create(name='Workout 1')
        self.workout2 = Workout.objects.create(name='Workout 2')
        self.account_workout1 = AccountWorkout.objects.create(account=self.user1, workout=self.workout1)
        self.account_workout2 = AccountWorkout.objects.create(account=self.user1, workout=self.workout2)

    def test_account_workout_creation(self):
        account_workout = AccountWorkout.objects.create(account=self.user2, workout=self.workout1)
        self.assertEqual(account_workout.account, self.user2)
        self.assertEqual(account_workout.workout, self.workout1)

    def test_account_workout_uniqueness(self):
        with self.assertRaises(Exception):
            AccountWorkout.objects.create(account=self.user1, workout=self.workout1)

    def test_account_workout_deletion(self):
        account_workout_id = self.account_workout1.id
        self.account_workout1.delete()
        with self.assertRaises(AccountWorkout.DoesNotExist):
            AccountWorkout.objects.get(id=account_workout_id)