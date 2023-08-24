from django.urls import path

from . import views

urlpatterns = [
    path(
        "dropdown",
        views.DropdownMenu.as_view(),
        name="dropdown"
    ),
    path(
        "workout-home",
        views.WorkoutListView.as_view(),
        name="workout-home"
    ),
    path(
        "",
        views.EntryListView.as_view(),
        name="entry-list"
    ),
    path(
        "entry/<int:pk>",
        views.EntryDetailView.as_view(),
        name="entry-detail"
    ),
    path(
        "buildworkout",
        views.BuildWorkoutCreateView.as_view(),
        name="buildworkout"
    ),
    path(
        "create",
        views.EntryCreateView.as_view(),
        name="entry-create"
    ),
    path(
        "entry/<int:pk>/update",
        views.EntryUpdateView.as_view(),
        name="entry-update",
    ),
    path(
        "entry/<int:pk>/delete",
        views.EntryDeleteView.as_view(),
        name="entry-delete",
    ),
]