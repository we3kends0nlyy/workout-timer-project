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
from django.db.utils import OperationalError
from django.db import transaction
from .forms import DropdownMenuForm, DropdownUpdateMinutesMenuForm, DropdownUpdateSecondsMenuForm
from .models import Entry
import sqlite3



class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["exercise", "order_in_workout"]
        
        labels = {
            "exercise": "Exercise/Activity",
            "order_in_workout": "Order in workout",
        }
        
        help_texts = {
            "exercise": "Enter your exercise or break activity here.",
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
            exercise = connection.execute('SELECT exercise FROM entries_entry ORDER BY id DESC LIMIT 1;')
            exercise_type = exercise.fetchone()[0]
            connection.execute('UPDATE entries_entry SET seconds = :seconds WHERE exercise = :exercise;', {'seconds': selected_option_seconds, 'exercise': exercise_type})
            connection.execute('UPDATE entries_entry SET minutes = :minutes WHERE exercise = :exercise;', {'minutes': selected_option_minutes, 'exercise': exercise_type})
            connection.commit()


            return redirect('entry-list')
        return render(request, self.template_name, {'form': form})


class DropdownUpdateMenu(View):

    template_name = 'entries/entry_update_times.html'
    model = Entry

    def __init__(self) -> None:
        self.entry_id = None

    def get(self, request, *args, **kwargs):
        seconds = self.kwargs['seconds']
        form = DropdownUpdateSecondsMenuForm(initial={'seconds': seconds})
        return render(request, self.template_name, {'form': form})

    def get_id(self, request, *args, **kwargs):
        return self.kwargs['id']

    def post(self, request, *args, **kwargs):
        form = DropdownUpdateSecondsMenuForm(request.POST)
        if form.is_valid():
            selected_option_seconds = form.cleaned_data['seconds']
            connection = sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None)
            cursor = connection.execute('PRAGMA foreign_keys = ON;')
            connection.commit()
            cursor.close()
            connection.execute('UPDATE entries_entry SET seconds = :seconds WHERE id = :id;', {'seconds': selected_option_seconds, 'id': self.get_id(0)})
            connection.commit()
            return redirect('entry-list')
        return render(request, self.template_name, {'form': form})


class DropdownUpdateMinutesMenu(View):

    template_name = 'entries/entry_update_times.html'
    model = Entry
    
    def __init__(self):
        self.entry_id = None

    def get(self, request, *args, **kwargs):
        minutes = self.kwargs['minutes']
        form = DropdownUpdateMinutesMenuForm(initial={'minutes': minutes})
        return render(request, self.template_name, {'form': form})
    
    def get_id(self, request, *args, **kwargs):
        return self.kwargs['id']


    def post(self, request, *args, **kwargs):
        form = DropdownUpdateMinutesMenuForm(request.POST)
        if form.is_valid():
            selected_option_minutes = form.cleaned_data['minutes']
            connection = sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None)
            cursor = connection.execute('PRAGMA foreign_keys = ON;')
            connection.commit()
            cursor.close()
            connection.execute('UPDATE entries_entry SET minutes = :minutes WHERE id = :id;', {'minutes': selected_option_minutes, 'id': self.get_id(0)})
            connection.commit()
            return redirect('entry-list')
        return render(request, self.template_name, {'form': form})



class BuildWorkoutCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'buildworkout/buildworkout.html' 
    success_url = reverse_lazy("dropdown")
    success_message = "Your new entry was created!"

    def form_valid(self, form):
        workout = form.cleaned_data['exercise']

        new_entry = form.save(commit=False)
        new_order_of_workout = new_entry.order_in_workout
        existing_entry = Entry.objects.filter(order_in_workout=new_order_of_workout).first()
        real_id = True
        while real_id is not None:
            with sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None) as connection:
                connection.execute('PRAGMA foreign_keys = ON;')
                real_id = self.find_matching_order(connection, new_order_of_workout)
                print("DONEDONEDONEDONE")
                '''
                if real_id is not None:
                    cursor = connection.cursor()
                    cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_order_of_workout)+1, 'id': real_id[0]})
                    connection.commit()
                    cursor.close()
                    new_order_of_workout = int(new_order_of_workout)+1
                    real_id = self.find_matching_order(connection, new_order_of_workout)
                '''
        return super().form_valid(form)

    def find_matching_order(self, connection, new_order_of_workout):
        cursor = connection.cursor()
        cursor.execute('SELECT id, exercise FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':new_order_of_workout})
        real_id = cursor.fetchone()
        connection.commit()
        cursor.close()
        self.check_if_real_id_is_not_none(connection, new_order_of_workout, real_id)



    def check_if_real_id_is_not_none(self, connection, new_order_of_workout, real_id):
        if real_id is not None:
            print(real_id, "THE REAL ONESS")
            real_id, new_order_of_workout = self.check_for_one_more_up(connection, int(new_order_of_workout)+1)
            self.check_if_real_id_is_not_none(connection, new_order_of_workout, real_id)
        else:
            self.update_order(connection, new_order_of_workout, real_id)
    

    def check_for_one_more_up(self, connection, new_order_of_workout):
        cursor = connection.cursor()
        cursor.execute('SELECT id, exercise FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':new_order_of_workout})
        real_id = cursor.fetchone()
        connection.commit()
        cursor.close()
        yield from (real_id, new_order_of_workout)

    def update_order(self, connection, new_order_of_workout, real_id):
            print(real_id, "EEEEEEEE")
            cursor = connection.cursor()
            cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_order_of_workout)+1, 'id': real_id})
            connection.commit()
            cursor.close()
            new_order_of_workout = int(new_order_of_workout)+1
            

class EntryListView(LockedView, ListView):
    model = Entry
    queryset = Entry.objects.all().order_by('order_in_workout')
    template_name = 'entries/entry_list.html'





class EntryDetailView(LockedView, DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'

class EntryOrderDetailView(LockedView, DetailView):
    model = Entry
    template_name = 'entries/entryorder_detail.html'

class EntryTimeDetailView(LockedView, DetailView):
    model = Entry
    template_name = 'entries/entrytime_detail.html'

class EntryCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    fields = ["exercise", "order_in_workout"]
    success_url = reverse_lazy("entry-list")
    success_message = "Your new entry was created!"


class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["exercise"]
    success_message = "Your entry was updated!"
    template_name = 'entries/entry_form.html'

    def get_success_url(self):
        return reverse_lazy("entry-detail", kwargs={"pk": self.object.pk})

class EntryUpdateView2(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["order_in_workout"]
    success_message = "Your entry was updated!"
    template_name = 'entries/entry_update_view.html'

    def get_success_url(self):
        return reverse_lazy("entryorder-detail", kwargs={"pk": self.object.pk})



class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your entry was deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)