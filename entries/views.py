from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django import forms
from .forms import DropdownMenuForm
from .models import Entry, Time, Workouts

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


class DropdownMenu(View):
    template_name = 'buildworkout/dropdown.html'
    model = Workouts

    def get(self, request, *args, **kwargs):
        form = DropdownMenuForm()  # Initialize the form

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DropdownMenuForm(request.POST)
        if form.is_valid():
            selected_option_seconds = form.cleaned_data['seconds']
            selected_option_minutes = form.cleaned_data['minutes']
            print(selected_option_seconds, selected_option_minutes)

            return redirect('entry-list')  # Redirect to the desired URL
        return render(request, self.template_name, {'form': form})


class BuildWorkoutCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'buildworkout/buildworkout.html'
    success_url = reverse_lazy("dropdown")
    success_message = "Your new entry was created!"



class EntryListView(LockedView, ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")


class EntryDetailView(LockedView, DetailView):
    model = Entry



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
