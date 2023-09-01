from typing import Any, Dict, Optional
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
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
from django.db import models, transaction
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
        form = DropdownMenuForm()
        connection = sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None)
        cursor = connection.execute('PRAGMA foreign_keys = ON;')
        connection.commit()
        cursor.close()
        exercise = connection.execute('SELECT exercise FROM entries_entry ORDER BY id DESC LIMIT 1;')
        exercise_type = exercise.fetchone()[0]
        connection.execute('UPDATE entries_entry SET seconds = :seconds WHERE exercise = :exercise;', {'seconds': 0, 'exercise': exercise_type})
        connection.execute('UPDATE entries_entry SET minutes = :minutes WHERE exercise = :exercise;', {'minutes': 0, 'exercise': exercise_type})
        connection.commit()
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

    def __init__(self) -> None:
        self.ids = []

    def __init__(self) -> None:
        self.ids = []

    def form_valid(self, form):
        build_object = BuildWorkoutCreateView()
        new_entry = form.save(commit=False)
        new_order_of_workout = new_entry.order_in_workout
        real_id = True
        while real_id is not None:
            with sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None) as connection:
                connection.execute('PRAGMA foreign_keys = ON;')
                real_id = self.find_matching_order(connection, new_order_of_workout, build_object)
        return super().form_valid(form)

    def find_matching_order(self, connection, new_order_of_workout, build_object):
        cursor = connection.cursor()
        cursor.execute('SELECT id, exercise FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':new_order_of_workout})
        real_id = cursor.fetchone()
        connection.commit()
        cursor.close()
        self.check_if_real_id_is_not_none(connection, new_order_of_workout, real_id, build_object)



    def check_if_real_id_is_not_none(self, connection, new_order_of_workout, real_id, build_object):
        if real_id is not None:
            build_object.ids.append(real_id[0])
            real_id, new_order_of_workout = self.check_for_one_more_up(connection, int(new_order_of_workout)+1)
            self.check_if_real_id_is_not_none(connection, new_order_of_workout, real_id, build_object)
        else:
            self.update_order(connection, new_order_of_workout, real_id, build_object)


    def check_for_one_more_up(self, connection, new_order_of_workout):
        cursor = connection.cursor()
        cursor.execute('SELECT id, exercise FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':new_order_of_workout})
        real_id = cursor.fetchone()
        connection.commit()
        cursor.close()
        yield from (real_id, new_order_of_workout)
 
    def update_order(self, connection, new_order_of_workout, real_id, build_object):
            cursor = connection.cursor()
            print(build_object.ids)
            num_of_entries = len(build_object.ids)
            for i in range(num_of_entries):
                print(num_of_entries, i, new_order_of_workout)
                cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_order_of_workout-i), 'id': build_object.ids[-1-i]})
                connection.commit()
            cursor.close()


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
    original_entry = None
    original_num = None

    def __init__(self) -> None:
        self.ids = []

    def get_success_url(self):
        return reverse_lazy("entryorder-detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        self.original_entry = super().get_object(queryset)
        EntryUpdateView2.original_num = self.original_entry.order_in_workout
        print(self.original_entry.order_in_workout)
        return self.original_entry
        

    def form_valid(self, form):
        build_object = EntryUpdateView2()
        new_entry = form.save(commit=False)
        new_order_of_workout = new_entry.order_in_workout
        new_order_id = new_entry.id
        print(new_order_of_workout, EntryUpdateView2.original_num, "yayayaya")
        existing_entry = Entry.objects.filter(order_in_workout=new_order_of_workout).first()
        real_id = True
        real_id2 = None
        while real_id is not None:
            with sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None) as connection:
                connection.execute('PRAGMA foreign_keys = ON;')
                real_id = self.find_matching_order(connection, new_order_of_workout, EntryUpdateView2.original_num, build_object, new_order_id, new_entry)
        return super().form_valid(form)

    def find_matching_order(self, connection, new_order_of_workout, orig_workout_num, build_object, new_order_id, new_entry):
        cursor = connection.cursor()
        cursor.execute('SELECT id, exercise FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':new_order_of_workout})
        real_id = cursor.fetchone()
        connection.commit()
        cursor.close()
        if new_order_of_workout <= orig_workout_num:
            self.check_if_real_id_is_not_none(connection, new_order_of_workout, orig_workout_num, real_id, build_object, new_order_id, new_entry)
        if new_order_of_workout > orig_workout_num:
            self.check_if_real_id_down_is_not_none(connection, new_order_of_workout, orig_workout_num, real_id, build_object, new_order_id, new_entry)
        



    def check_if_real_id_is_not_none(self, connection, new_order_of_workout, orig_num_workout, real_id, build_object, new_order_id, new_entry):
        if real_id is not None:
            build_object.ids.append(real_id[0])
            real_id, new_order_of_workout = self.check_for_one_more_up(connection, int(new_order_of_workout)+1)
            self.check_if_real_id_is_not_none(connection, new_order_of_workout, orig_num_workout, real_id, build_object, new_order_id, new_entry)
        else:
            self.update_order(connection, new_order_of_workout, len(build_object.ids), orig_num_workout, real_id, build_object, "up", new_order_id, new_entry)

    def check_if_real_id_down_is_not_none(self, connection, new_order_of_workout, orig_num_workout, real_id, build_object, new_order_id, new_entry):
        if real_id is not None:
            build_object.ids.append(real_id[0])
            real_id, new_order_of_workout = self.check_for_one_more_up(connection, int(new_order_of_workout)-1)
            self.check_if_real_id_down_is_not_none(connection, new_order_of_workout, orig_num_workout, real_id, build_object, new_order_id, new_entry)
        else:
            self.update_order(connection, new_order_of_workout, len(build_object.ids), orig_num_workout, real_id, build_object, "down", new_order_id, new_entry)


    def check_for_one_more_up(self, connection, new_order_of_workout):
        cursor = connection.cursor()
        cursor.execute('SELECT id, exercise FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':new_order_of_workout})
        real_id = cursor.fetchone()
        connection.commit()
        cursor.close()
        yield from (real_id, new_order_of_workout)

    def update_order(self, connection, new_order_of_workout, leng, orig_num_workout, real_id, build_object, up_or_down, new_order_id, new_entry):
            cursor = connection.cursor()
            num_of_entries = len(build_object.ids)
            if len(build_object.ids) == 0:
                cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': new_order_of_workout, 'id': new_order_id})
                connection.commit()
            if up_or_down == "down" and len(build_object.ids) != 0:
                print(build_object.ids, 'LISTLISTLIST2')
                for i in range(1, ((new_entry.order_in_workout-orig_num_workout)+1)):
                    print(i, new_entry.order_in_workout)
                    cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_entry.order_in_workout-i), 'id': build_object.ids[i-1]})
                    connection.commit()
                #cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(leng), 'id': build_object.ids[-1]})
                #connection.commit()
            if up_or_down == "up" and len(build_object.ids) != 0:
                print(build_object.ids, 'LISTIST')
                for i in range(1, ((orig_num_workout-new_entry.order_in_workout)+1)):
                    print(num_of_entries, i, new_entry.order_in_workout)
                    print(orig_num_workout, "ORIG")
                    try:
                        cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_entry.order_in_workout+i), 'id': build_object.ids[i-1]})
                        connection.commit()
                    except IndexError:
                        continue
            cursor.execute('SELECT COUNT(*) FROM entries_entry')
            num_of_exercises = cursor.fetchone()
            if new_entry.order_in_workout - 1 > num_of_exercises[0]:
                for order in range(2, new_entry.order_in_workout):
                    cursor.execute('SELECT id FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':order})
                    does_id_exist = cursor.fetchone()
                    connection.commit()
                    if does_id_exist is not None:
                        print(does_id_exist[0], "EXIST:?")
                        lowest_order = self.search_for_lowest_order(connection, order-1)
                        if lowest_order is not None:
                            cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': lowest_order, 'id': does_id_exist[0]})
                            connection.commit() 
                    else:
                        continue
                cursor.close()
    def search_for_lowest_order(self, connection, order, lowest_id=None):
        cursor = connection.cursor()
        if lowest_id is None or order != 1:
            print(lowest_id, order, "ORDER")
            cursor.execute('SELECT id FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout': order})
            lowest_id = cursor.fetchone()
            connection.commit()
            order -= 1
            self.search_for_lowest_order(connection, order, lowest_id)
        else:
            return order






class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your entry was deleted!"
    self_object = None

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleted_object'] = self.object
        EntryDeleteView.self_object = self.object
        result = True
        current_order = int(EntryDeleteView.self_object.order_in_workout) + 1
        with sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None) as connection:
            connection.execute('PRAGMA foreign_keys = ON;')
            cursor = connection.cursor()
            while result is not None:
                cursor.execute('SELECT id FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout': current_order})
                id_num = cursor.fetchone()
                try:
                    result = cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': current_order-1, 'id': id_num[0]})
                    print("hi")
                    print(result.fetchone(), "RESULT")
                    connection.commit()
                    current_order += 1
                except TypeError as e:
                    print(e)
                    cursor.close()
                    result = None
        cursor.close()
        return super().get_context_data(**kwargs)