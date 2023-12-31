
from django.urls import path, include

from . import views

urlpatterns = [
    path(
        "dropdown",
        views.DropdownMenu.as_view(),
        name="dropdown"
    ),
    path(
        "dropdown/<int:seconds>/<int:id>/update",
        views.DropdownUpdateMenu.as_view(),
        name="dropdown-update"
    ),
    path(
        "dropdown<int:minutes>/<int:id>/updatemins",
        views.DropdownUpdateMinutesMenu.as_view(),
        name="dropdown-update-minutes"
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
        "entrytime-detail/<int:pk>",
        views.EntryTimeDetailView.as_view(),
        name='entrytime-detail'
    ),
    path(
        "entryorder-detail/<int:pk>",
        views.EntryOrderDetailView.as_view(),
        name="entryorder-detail"
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
        "entry/<int:pk>/update2",
        views.EntryUpdateView2.as_view(),
        name="entry-update2",
    ),
    path(
        "entry/<int:pk>/delete",
        views.EntryDeleteView.as_view(),
        name="entry-delete",
    ),
    path(
        "workout",
        views.WorkoutGo.as_view(),
        name="workout",
    ),
    path(
        'get-exercise-data/',
        views.get_exercise_data,
        name='get-exercise-data'),
    path(
        'choose-prev',
        views.ChooseWorkout.as_view(),
        name='choose-prev'),
    path(
        'premade',
        views.Premade.as_view(),
        name='premade'),
    path(
        'clear-all',
        views.clear_all,
        name='clear-all'),
]