from rest_framework import serializers
from workout_tracker.models import Exercise, Workout

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [ 'name', 'description', 'image', 'video']
        read_only_fields = ('id',)


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = [ 'name', 'description', 'exercises']
        read_only_fields = ('id',)

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', None )
        workout = Workout.objects.create(**validated_data)
        if exercises_data is not  None:
            for exercise_data in exercises_data:
                exercise = Exercise.objects.create(**exercise_data)
                workout.exercises.add(exercise)
        return workout