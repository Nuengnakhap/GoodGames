"""
    `forms.py`
    Contains classes to create forms
"""

import datetime

from django import forms
from django.core.exceptions import ValidationError

from dayoff.models import DayOff


class DayOffForm(forms.ModelForm):
    class Meta:
        model = DayOff
        exclude = ['approve_status', 'created_by']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    error = None

    def clean(self):
        data = super().clean()

        start = data.get('date_start')
        end = data.get('date_end')

        if start > end:
            self.error = 'วัน - เวลาไม่ถูกต้อง'
            raise ValidationError('')
        elif start < datetime.datetime.now().date():
            self.error = 'ไม่สามารถเลือกวันในอดีตได้'
            raise ValidationError('')