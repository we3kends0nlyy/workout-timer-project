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
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django import forms
from .forms import DropdownMenuForm, DropdownUpdateMinutesMenuForm, DropdownUpdateSecondsMenuForm, ChoosePrevWorkout, PremadeForm
from .models import Entry, ExistingEntry1, ExistingEntry2, ExistingEntry3, ExistingEntry4, ExistingEntry5, GoWorkout, Premade1, Premade2, Premade3, Premade4, Premade5
import sqlite3
from django.http import JsonResponse
from .models import Entry
from pathlib import Path

BASE_DIR2 = Path(__file__).resolve().parent


def get_exercise_data(request):
    exercises = GoWorkout.objects.all()
    exercise_data = [
        {'exercise': exercise.exercise, 'time': float(exercise.seconds) + float(int(exercise.minutes) * 60), 'order_in_workout': exercise.order_in_workout}
        for exercise in exercises
    ]
    exercise_data = sorted(exercise_data, key=lambda x: x['order_in_workout'])
    return JsonResponse({'exerciseData': exercise_data})



def clear_all(request):
    connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
    connection.execute('DELETE FROM entries_entry;')
    connection.execute('DELETE FROM entries_existingentry1;')
    connection.execute('DELETE FROM entries_existingentry2;')
    connection.execute('DELETE FROM entries_existingentry3;')
    connection.execute('DELETE FROM entries_existingentry4;')
    connection.execute('DELETE FROM entries_existingentry5;')
    return redirect('entry-list')

class ChooseWorkout(View):
    template_name = 'entries/choose_prev.html'

    def get(self, request, *args, **kwargs):

        entry_data = Entry.objects.all().order_by('order_in_workout')
        existing_entry1 = ExistingEntry1.objects.all().order_by('order_in_workout')
        existing_entry2 = ExistingEntry2.objects.all().order_by('order_in_workout')
        existing_entry3 = ExistingEntry3.objects.all().order_by('order_in_workout')
        existing_entry4 = ExistingEntry4.objects.all().order_by('order_in_workout')
        existing_entry5 = ExistingEntry5.objects.all().order_by('order_in_workout')
        if len(existing_entry1) == 0:
            messages.error(self.request, "You must add to your own workout and start it before you can access this page.")
            return redirect('entry-list') 
        else:
            form = ChoosePrevWorkout()

            context = {
                'entry_data': entry_data,
                'existing_entry1': existing_entry1,
                'existing_entry2': existing_entry2,
                'existing_entry3': existing_entry3,
                'existing_entry4': existing_entry4,
                'existing_entry5': existing_entry5,
                'form': form,
            }


            return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
        form = ChoosePrevWorkout(request.POST)
        if form.is_valid():
            workout_choice = form.cleaned_data['workouts']
            connection.execute('DELETE FROM entries_entry;')
            connection.execute(f"INSERT INTO entries_entry (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_existingentry{workout_choice};")
            connection.commit()
            return redirect('entry-list')
        return render(request, self.template_name, {'form': form})


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["exercise", "order_in_workout"]

        labels = {
            "exercise": "Exercise/Activity/Break",
            "order_in_workout": "Order in workout",
        }

        help_texts = {

        }


class LockedView(LoginRequiredMixin):
    login_url = "admin:login"


class DropdownMenu(View, SuccessMessageMixin):

    template_name = 'buildworkout/dropdown.html'
    model = Entry
    success_message = "Your exercise has been added to the workout!"

    def get(self, request, *args, **kwargs):
        form = DropdownMenuForm()
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
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


            connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
            cursor = connection.execute('PRAGMA foreign_keys = ON;')
            connection.commit()
            cursor.close()
            exercise = connection.execute('SELECT exercise, id FROM entries_entry ORDER BY id DESC LIMIT 1;')
            exercise_type = exercise.fetchone()

            order = connection.execute('SELECT order_in_workout FROM entries_entry WHERE id = :id;', {'id': exercise_type[1]})
            order_num = order.fetchone()

            connection.execute('UPDATE entries_entry SET seconds = :seconds WHERE exercise = :exercise;', {'seconds': selected_option_seconds, 'exercise': exercise_type[0]})
            connection.execute('UPDATE entries_entry SET minutes = :minutes WHERE exercise = :exercise;', {'minutes': selected_option_minutes, 'exercise': exercise_type[0]})
            connection.commit()

            messages.success(self.request, f"{exercise_type[0]} has been added to the workout at order #{order_num[0]}!")
            return redirect('entry-list')
        return render(request, self.template_name, {'form': form})


class DropdownUpdateMenu(View, SuccessMessageMixin):

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
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
        minutes = connection.execute('SELECT minutes FROM entries_entry WHERE id = :id', {'id':self.get_id(0)})
        mins = minutes.fetchone()
        connection.commit()
        form = DropdownUpdateSecondsMenuForm(request.POST)
        if form.is_valid():
            selected_option_seconds = form.cleaned_data['seconds']
            if mins[0] == "0" and selected_option_seconds == "0":
                messages.error(self.request, 'You cannot change seconds to 0 when minutes is already 0.')
                return redirect('entry-list')
            else:
                connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
                cursor = connection.execute('PRAGMA foreign_keys = ON;')
                connection.commit()
                cursor.close()
                connection.execute('UPDATE entries_entry SET seconds = :seconds WHERE id = :id;', {'seconds': int(selected_option_seconds), 'id': self.get_id(0)})
                item = connection.execute('SELECT exercise FROM entries_entry WHERE id = :id', {'id':self.get_id(0)})
                workout = item.fetchone()
                time = selected_option_seconds
                connection.commit()
                messages.success(self.request, f"{workout[0]} has been updated to {time} seconds.")
                connection.commit()
                return redirect('entry-list')
        return render(request, self.template_name, {'form': form})

class DropdownUpdateMinutesMenu(View):

    template_name = 'entries/entry_update_times_minutes.html'
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
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
        seconds = connection.execute('SELECT seconds FROM entries_entry WHERE id = :id', {'id':self.get_id(0)})
        secs = seconds.fetchone()
        connection.commit()
        form = DropdownUpdateMinutesMenuForm(request.POST)
        if form.is_valid():
            selected_option_minutes = form.cleaned_data['minutes']
            if secs[0] == "0" and selected_option_minutes == "0":
                messages.error(self.request, f"You cannot change minutes to 0 when seconds is already 0.")
                return redirect('entry-list')
            else:
                connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
                cursor = connection.execute('PRAGMA foreign_keys = ON;')
                connection.commit()
                cursor.close()
                connection.execute('UPDATE entries_entry SET minutes = :minutes WHERE id = :id;', {'minutes': int(selected_option_minutes), 'id': self.get_id(0)})
                item = connection.execute('SELECT exercise FROM entries_entry WHERE id = :id', {'id':self.get_id(0)})
                workout = item.fetchone()
                time = selected_option_minutes
                connection.commit()
                messages.success(self.request, f"{workout[0]} has been updated to {time} minutes.")
                connection.commit()
                return redirect('entry-list')
        return render(request, self.template_name, {'form': form})



class BuildWorkoutCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'buildworkout/buildworkout.html' 
    success_url = reverse_lazy("dropdown")
    def __init__(self) -> None:
        self.ids = []

    def __init__(self) -> None:
        self.ids = []

    def form_valid(self, form):
        build_object = BuildWorkoutCreateView()
        new_entry = form.save(commit=False)
        new_order_of_workout = new_entry.order_in_workout
        real_id = True
        if new_order_of_workout < 1:
            messages.error(self.request, "The order should be a number greater than 0.")
            return redirect('buildworkout')
        else:
            while real_id is not None:
                with sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None) as connection:
                    connection.execute('PRAGMA foreign_keys = ON;')
                    real_id = self.find_matching_order(connection, new_order_of_workout, build_object)
                    cursor = connection.cursor()
                    cursor.execute('SELECT COUNT(*) FROM entries_entry')
                    num_of_exercises = cursor.fetchone()
                    if new_order_of_workout > num_of_exercises[0]:
                        new_order_of_workout = num_of_exercises[0] + 1
                        form.instance.order_in_workout = num_of_exercises[0] + 1
                        form.save(commit=False)
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
            num_of_entries = len(build_object.ids)
            for i in range(num_of_entries):
                cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_order_of_workout-i), 'id': build_object.ids[-1-i]})
                connection.commit()
            cursor.close()


class EntryListView(ListView, View):
    model = Entry
    queryset = Entry.objects.all().order_by('order_in_workout')
    template_name = 'entries/entry_list.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
        isit = connection.execute('SELECT id FROM entries_entry WHERE minutes = :minutes AND seconds = :seconds;', {'minutes':0, 'seconds':0})
        id = isit.fetchone()
        if id is not None:
            connection.execute('DELETE FROM entries_entry WHERE id = :id;', {'id': id[0]})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
        cursor = connection.execute('PRAGMA foreign_keys = ON;')
        connection.commit()
        cursor.close()
        num = connection.execute('SELECT COUNT(*) FROM entries_entry')
        nums = num.fetchone()[0]
        if nums == 0:
            messages.error(self.request, "You must add an exercise to the workout before starting!")
            return redirect('entry-list')
        else:
            return redirect('workout')
        

class WorkoutGo(View, SuccessMessageMixin):
    model = Entry
    template_name = 'entries/workout.html'
    def get(self, request, *args, **kwargs):
        form = DropdownMenuForm()
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
        connection.execute('DELETE FROM entries_existingentry5;')
        connection.execute('INSERT INTO entries_existingentry5 (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_existingentry4;')
        connection.execute('DELETE FROM entries_existingentry4;')
        connection.execute('INSERT INTO entries_existingentry4 (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_existingentry3;')
        connection.execute('DELETE FROM entries_existingentry3;')
        connection.execute('INSERT INTO entries_existingentry3 (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_existingentry2;')
        connection.execute('DELETE FROM entries_existingentry2;')
        connection.execute('INSERT INTO entries_existingentry2 (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_existingentry1;')
        connection.execute('DELETE FROM entries_existingentry1;')
        connection.execute('INSERT INTO entries_existingentry1 (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_entry;')
        connection.execute('DELETE FROM entries_goworkout;')
        connection.execute('INSERT INTO entries_goworkout (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_entry;')
        connection.execute('DELETE FROM entries_entry;')
        connection.commit()
        return render(request, self.template_name, {'form': form})



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
    success_message = "Your exercise was added to the workout!!"


class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["exercise"]
    success_message = "Your exercise was updated!"
    template_name = 'entries/entry_form.html'

    def get_success_url(self):
        return reverse_lazy("entry-list")

class EntryUpdateView2(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["order_in_workout"]
    success_message = "Your exercise was updated!"
    template_name = 'entries/entry_update_view.html'
    original_entry = None
    original_num = None
    new_order = None
    num_of_exercises = None

    def __init__(self) -> None:
        self.ids = []

    def get_success_url(self):
        return reverse_lazy("entry-list")

    def get_object(self, queryset=None):
        self.original_entry = super().get_object(queryset)
        EntryUpdateView2.original_num = self.original_entry.order_in_workout
        return self.original_entry


    def form_valid(self, form):
        build_object = EntryUpdateView2()
        new_entry = form.save(commit=False)
        new_order_of_workout = new_entry.order_in_workout
        new_order_id = new_entry.id
        real_id = True
        real_id2 = None
        while real_id is not None:
            with sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None) as connection:
                connection.execute('PRAGMA foreign_keys = ON;')
                cursor = connection.cursor()
                cursor.execute('SELECT COUNT(*) FROM entries_entry')
                EntryUpdateView2.num_of_exercises = cursor.fetchone()
                real_id = self.find_matching_order(connection, new_order_of_workout, EntryUpdateView2.original_num, build_object, new_order_id, new_entry)
        if EntryUpdateView2.new_order is not None:
            print(EntryUpdateView2.new_order, EntryUpdateView2.num_of_exercises[0])
            if EntryUpdateView2.new_order - 1 == EntryUpdateView2.num_of_exercises[0]:
                form.instance.order_in_workout = EntryUpdateView2.new_order - 1
                form.save(commit=False)
            else:
                form.instance.order_in_workout = EntryUpdateView2.new_order
                form.save(commit=False)
        if EntryUpdateView2.original_num == 1:
            for i in range(1, int(EntryUpdateView2.new_order) + 1):
                cursor = connection.cursor()
                if new_order_of_workout == len(build_object.ids):
                    cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout_new WHERE order_in_workout = :i;', {'i': i, 'order_in_workout_new': i})
                    connection.commit() 
                else:
                    print(i)
                    cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout_new WHERE order_in_workout = :i;', {'i': i, 'order_in_workout_new': i-1})
                    connection.commit()
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
            EntryUpdateView2.new_order = None
            cursor = connection.cursor()
            num_of_entries = len(build_object.ids)
            if len(build_object.ids) == 0:
                cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': new_order_of_workout, 'id': new_order_id})
                connection.commit()
            if up_or_down == "down" and len(build_object.ids) != 0:
                for i in range(1, ((new_entry.order_in_workout-orig_num_workout)+1)):
                    cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_entry.order_in_workout-i), 'id': build_object.ids[i-1]})
                    connection.commit()
            if up_or_down == "up" and len(build_object.ids) != 0:
                for i in range(1, ((orig_num_workout-new_entry.order_in_workout)+1)):
                    try:
                        cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': int(new_entry.order_in_workout+i), 'id': build_object.ids[i-1]})
                        connection.commit()
                    except IndexError:
                        continue
            if new_entry.order_in_workout - 1 > EntryUpdateView2.num_of_exercises[0]:
                for order in range(2, new_entry.order_in_workout+1):
                    cursor.execute('SELECT id FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':order})
                    does_id_exist = cursor.fetchone()
                    connection.commit()
                    if does_id_exist is not None:
                        order = self.search_for_lowest_order(connection, order-1)
                        cursor.execute('SELECT id FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout':order})
                        does_it_equal_one = cursor.fetchone()
                        connection.commit()
                        if does_it_equal_one is None:
                            cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': order, 'id': does_id_exist[0]})
                            connection.commit() 
                        else:
                            continue
                    else:
                        continue
                cursor.close()
                if EntryUpdateView2.original_num == 1:
                    EntryUpdateView2.new_order = order - 1
                else:
                    EntryUpdateView2.new_order = order
            if EntryUpdateView2.new_order is None:
                if EntryUpdateView2.original_num == 1:
                    EntryUpdateView2.new_order = new_entry.order_in_workout

    def search_for_lowest_order(self, connection, order, lowest_id=None):
        cursor = connection.cursor()
        while lowest_id is None and order >= 1:
            cursor.execute('SELECT id FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout': order})
            lowest_id = cursor.fetchone()
            connection.commit()
            order -= 1
        return order+2



class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your exercise/break was deleted from the workout!"
    self_object = None
    current_order = None
    result = True

    def delete(self, request, *args, **kwargs):
        with sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None) as connection:
            connection.execute('PRAGMA foreign_keys = ON;')
            cursor = connection.cursor()
            while EntryDeleteView.result is not None:
                cursor.execute('SELECT id FROM entries_entry WHERE order_in_workout = :order_in_workout;', {'order_in_workout': EntryDeleteView.current_order})
                id_num = cursor.fetchone()
                try:
                    EntryDeleteView.result = cursor.execute('UPDATE entries_entry SET order_in_workout = :order_in_workout WHERE id = :id;', {'order_in_workout': EntryDeleteView.current_order-1, 'id': id_num[0]})
                    connection.commit()
                    EntryDeleteView.current_order += 1
                except TypeError as e:
                    cursor.close()
                    break
                    result = None
        messages.success(self.request, self.success_message)
        cursor.close()
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleted_object'] = self.object
        EntryDeleteView.self_object = self.object
        EntryDeleteView.current_order = int(EntryDeleteView.self_object.order_in_workout) + 1
        return super().get_context_data(**kwargs)
    

class Premade(View):
    template_name = 'entries/premade.html'

    def get(self, request, *args, **kwargs):

        entry_data = Entry.objects.all().order_by('order_in_workout')
        premade1 = Premade1.objects.all().order_by('order_in_workout')
        premade2 = Premade2.objects.all().order_by('order_in_workout')
        premade3 = Premade3.objects.all().order_by('order_in_workout')
        premade4 = Premade4.objects.all().order_by('order_in_workout')
        premade5 = Premade5.objects.all().order_by('order_in_workout')
        form = PremadeForm()

        context = {
            'entry_data': entry_data,
            'premade1': premade1,
            'premade2': premade2,
            'premade3': premade3,
            'premade4': premade4,
            'premade5': premade5,
            'form': form,
        }


        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        connection = sqlite3.connect(BASE_DIR2 / "workouts2.db", isolation_level=None)
        form = PremadeForm(request.POST)
        if form.is_valid():
            workout_choice = form.cleaned_data['workouts']
            connection.execute('DELETE FROM entries_entry;')
            connection.execute(f"INSERT INTO entries_entry (exercise, order_in_workout, seconds, minutes) SELECT exercise, order_in_workout, seconds, minutes FROM entries_premade{workout_choice};")
            connection.commit()
            return redirect('entry-list')
        return render(request, self.template_name, {'form': form})
