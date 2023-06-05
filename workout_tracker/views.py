from rest_framework import generics, permissions
from workout_tracker.models import Exercise, Workout
from workout_tracker.serializers import ExerciseSerializer, WorkoutSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnly(BasePermission):
    """
    Allows read-only access to a view.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsTrainer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer


class ExerciseList(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.AllowAny]

class ExerciseCreate(generics.CreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [ permissions.IsAuthenticated,IsTrainer]

class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [ IsTrainer  | ReadOnly]

class WorkoutList(generics.ListAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.AllowAny]

class WorkoutCreate(generics.CreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsTrainer]

class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsTrainer | ReadOnly]


class UserWorkoutsView(generics.ListAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.workouts.all()