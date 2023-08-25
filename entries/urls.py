from django.urls import path

from . import views

urlpatterns = [
    path(
        "dropdown",
        views.DropdownMenu.as_view(),
        name="dropdown"
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
]