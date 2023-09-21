from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
import sqlite3
from .models import Entry, ExistingEntry1, ExistingEntry2, ExistingEntry3, ExistingEntry4, ExistingEntry5

class DropdownMenuForm(forms.Form):
    seconds = forms.ChoiceField(choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), 
                                         (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), 
                                         (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'),
                                           (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), 
                                           (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), 
                                           (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), 
                                           (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), 
                                           (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), 
                                           (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), 
                                           (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), 
                                           (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), 
                                           (56, '56'), (57, '57'), (58, '58'), (59, '59'), (60, '60')])
    minutes = forms.ChoiceField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), 
                                         (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), 
                                         (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'),
                                           (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), 
                                           (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), 
                                           (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), 
                                           (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), 
                                           (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), 
                                           (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), 
                                           (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), 
                                           (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), 
                                           (56, '56'), (57, '57'), (58, '58'), (59, '59'), (60, '60')])
    
    def clean(self):
        cleaned_data = super().clean()
        seconds = int(cleaned_data.get('seconds', 0))
        minutes = int(cleaned_data.get('minutes', 0))

        if seconds == 0 and minutes == 0:
            raise ValidationError("Please choose a time greater than zero.")

class DropdownUpdateSecondsMenuForm(forms.Form):
    seconds = forms.ChoiceField(choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), 
                                         (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), 
                                         (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'),
                                           (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), 
                                           (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), 
                                           (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), 
                                           (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), 
                                           (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), 
                                           (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), 
                                           (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), 
                                           (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), 
                                           (56, '56'), (57, '57'), (58, '58'), (59, '59'), (60, '60')])
    def clean(self):
        cleaned_data = super().clean()
        seconds = int(cleaned_data.get('seconds', 0))


class DropdownUpdateMinutesMenuForm(forms.Form):
    minutes = forms.ChoiceField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), 
                                         (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), 
                                         (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'),
                                           (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), 
                                           (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), 
                                           (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), 
                                           (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), 
                                           (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), 
                                           (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), 
                                           (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), 
                                           (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), 
                                           (56, '56'), (57, '57'), (58, '58'), (59, '59'), (60, '60')])

    def clean(self):
        cleaned_data = super().clean()
        minutes = int(cleaned_data.get('minutes', 0))

        #if minutes == 0:
            #raise ValidationError("Please choose a time greater than zero.")

class CheckWorkout(forms.Form):
    exercises = forms.ChoiceField

    def clean(self):
        cleaned_data = super().clean()
        connection = sqlite3.connect('/Users/we3kends0onlyy/Documents/workout-project/db.sqlite3', isolation_level=None)
        cursor = connection.execute('PRAGMA foreign_keys = ON;')
        connection.commit()
        cursor.close()
        num = connection.execute('SELECT COUNT(*) FROM entries_entry')
        nums = num.fetchone()[0]
        if nums == 0:
            raise ValidationError("You must add an exercise to the workout before starting!")
        


class ChoosePrevWorkout(forms.Form):
    workouts = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'style': 'width: 210px; height: 40px; font-size: 26px; margin-left: -43px'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        entry_data = Entry.objects.all().order_by('order_in_workout')
        existing_entry1 = ExistingEntry1.objects.all().order_by('order_in_workout')
        existing_entry2 = ExistingEntry2.objects.all().order_by('order_in_workout')
        existing_entry3 = ExistingEntry3.objects.all().order_by('order_in_workout')
        existing_entry4 = ExistingEntry4.objects.all().order_by('order_in_workout')
        existing_entry5 = ExistingEntry5.objects.all().order_by('order_in_workout')
        print(existing_entry1)
        options = []
        if len(existing_entry1) != 0:
            options.append(("1", "Workout 1"))
        if len(existing_entry2) != 0:
            options.append(("2", "Workout 2"))
        if len(existing_entry3) != 0:
            options.append(("3", "Workout 3"))
        if len(existing_entry4) != 0:
            options.append(("4", "Workout 4"))
        if len(existing_entry5) != 0:
            options.append(("5", "Workout 5"))
        self.fields['workouts'].choices = options
        
    def clean(self):
        cleaned_data = super().clean()
        workouts = int(cleaned_data.get('workouts', 0))
