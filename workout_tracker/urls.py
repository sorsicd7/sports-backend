from django.urls import path
from workout_tracker.views import (
    ExerciseList,
    ExerciseCreate,
    ExerciseDetail,
    WorkoutList,

)

urlpatterns = [
    path('exercises/', ExerciseList.as_view(), name='exercise-list'),
    path('exercises/create/', ExerciseCreate.as_view(), name='exercise-create'),
    path('exercises/<int:pk>/', ExerciseDetail.as_view(), name='exercise-detail'),
    path('workouts/', WorkoutList.as_view(), name='workout-list'),
 ]