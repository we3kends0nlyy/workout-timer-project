from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django import forms
from .models import Entry, Time

class DropdownMenu(ListView):
    template_name = 'buildworkout/dropdown.html'
    def get(self, request, *args, **kwargs):
        results = Time.objects.all()
        context = {"showseconds": results}
        return render(request, self.template_name, context)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "content"]
        
        labels = {
            "title": "Exercise/Activity",
            "content": "Time",
        }
        
        help_texts = {
            "title": "Enter your exercise or break activity here.",
            "content": "Enter a custom content description here.",
        }


class LockedView(LoginRequiredMixin):
    login_url = "admin:login"


class EntryListView(LockedView, ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")


class EntryDetailView(LockedView, DetailView):
    model = Entry


class BuildWorkoutCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'buildworkout/buildworkout.html'
    success_url = reverse_lazy("entry-list")
    success_message = "Your new entry was created!"


class EntryCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    fields = ["title", "content"]
    success_url = reverse_lazy("entry-list")
    success_message = "Your new entry was created!"


class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["title", "content"]
    success_message = "Your entry was updated!"

    def get_success_url(self):
        return reverse_lazy("entry-detail", kwargs={"pk": self.object.pk})


class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your entry was deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
