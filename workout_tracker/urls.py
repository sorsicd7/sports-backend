from django.urls import path
from workout_tracker.views import (
    ExerciseList,
    ExerciseCreate,
    ExerciseDetail,
    WorkoutList,
    WorkoutDetail,
    WorkoutCreate,
    UserWorkoutsView
)

urlpatterns = [
    path('exercises/', ExerciseList.as_view(), name='exercise-list'),
    path('exercises/create/', ExerciseCreate.as_view(), name='exercise-create'),
    path('exercises/<int:pk>/', ExerciseDetail.as_view(), name='exercise-detail'),
    path('workouts/', WorkoutList.as_view(), name='workout-list'),
    path('workouts/create/', WorkoutCreate.as_view(), name='workout-create'),
    path('workouts/<int:pk>/', WorkoutDetail.as_view(), name='workout-detail'),
    path('user-workouts/', UserWorkoutsView.as_view(), name='user-workouts'),
]