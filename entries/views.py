from typing import Any
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
from .models import Entry
import sqlite3

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["workout", "order_in_workout"]
        
        labels = {
            "workout": "Exercise/Activity",
            "order_in_workout": "Order in workout",
        }
        
        help_texts = {
            "workout": "Enter your exercise or break activity here.",
            "order_in_workout": "Enter the order in the workout you want this exercise to be.\nFor example if your workout so far is: 1. Push ups 2. Squats 3. Crunches, you can put  ",
        }


class LockedView(LoginRequiredMixin):
    login_url = "admin:login"


class DropdownMenu(View):

    template_name = 'buildworkout/dropdown.html'
    model = Entry

    def get(self, request, *args, **kwargs):
        form = DropdownMenuForm()  # Initialize the form

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DropdownMenuForm(request.POST)
        if form.is_valid():
            selected_option_seconds = form.cleaned_data['seconds']
            selected_option_minutes = form.cleaned_data['minutes']
            connection = sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None)
            cursor = connection.execute('PRAGMA foreign_keys = ON;')
            connection.commit()
            cursor.close()
            workout = connection.execute('SELECT workout FROM entries_entry ORDER BY id DESC LIMIT 1;')
            workout_type = workout.fetchone()[0]
            connection.execute('UPDATE entries_entry SET seconds = :seconds WHERE workout = :workout;', {'seconds': selected_option_seconds, 'workout': workout_type})
            connection.execute('UPDATE entries_entry SET minutes = :minutes WHERE workout = :workout;', {'minutes': selected_option_minutes, 'workout': workout_type})
            connection.commit()


            return redirect('entry-list')  # Redirect to the desired URL
        return render(request, self.template_name, {'form': form})




class BuildWorkoutCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'buildworkout/buildworkout.html' 
    success_url = reverse_lazy("dropdown")
    success_message = "Your new entry was created!"
    
    def form_valid(self, form):
        workout = form.cleaned_data['workout']
        return super().form_valid(form)



class EntryListView(LockedView, ListView):
    model = Entry
    queryset = Entry.objects.all()


class EntryDetailView(LockedView, DetailView):
    model = Entry



class EntryCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    fields = ["workout", "order_in_workout"]
    success_url = reverse_lazy("entry-list")
    success_message = "Your new entry was created!"


class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["workout", "order_in_workout"]
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
