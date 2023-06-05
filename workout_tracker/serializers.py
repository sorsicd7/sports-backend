from rest_framework import serializers
from workout_tracker.models import Exercise, Workout

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [ 'name', 'description', 'image', 'video']
        read_only_fields = ('id',)


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, required=False)

    class Meta:
        model = Workout
        fields = [ 'name', 'description', 'exercises']
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        exercises_data = validated_data.pop('exercises', None )
        workout = Workout.objects.create(**validated_data)
        if exercises_data is not  None:
            for exercise_data in exercises_data:
                exercise = Exercise.objects.create(**exercise_data)
                workout.exercises.add(exercise)
        if user :
            user.workouts.add(workout)
        return workout

    def update(self, instance, validated_data):
        # Update the fields of the Workout instance
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # Update the Exercise instances related to this Workout
        exercise_data = validated_data.pop('exercises', None)
        if exercise_data is not None:
            instance.exercises.clear()
            for exercise in exercise_data:
                if exercise.get('id'):
                    item = Exercise.objects.get(pk=exercise['id'])
                    item.name = exercise.get('name', item.name)
                    item.description = exercise.get('description', item.description)
                    item.save()
                    instance.exercises.add(item)
                else:
                    item = Exercise.objects.create(**exercise)
                    instance.exercises.add(item)
        instance.save()
        return instance