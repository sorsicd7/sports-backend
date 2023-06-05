from tkinter import N
from rest_framework import serializers
from workout_tracker.models import Exercise, Workout

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'image', 'video']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', None )
        workout = Workout.objects.create(**validated_data)
        if exercises_data is not  None:
            for exercise_data in exercises_data:
                exercise = Exercise.objects.get(id=exercise_data['id'])
                workout.exercises.add(exercise)
        return workout