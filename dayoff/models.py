from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class DayOff(models.Model):
    TYPE_CHOICES = (
        ('01', 'ลากิจ'),
        ('02', 'ลาป่วย')
    )

    APPROVE_STATUS_CHOICES = (
        (0, 'ไม่อนุมัติ'),
        (1, 'อนุมัติ'),
        (2, 'รอการอนุมัติ')
    )

    reason = models.TextField(null=False, blank=False)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, null=False, blank=False)
    date_start = models.DateField(null=False, blank=False)
    date_end = models.DateField(null=False, blank=False)
    approve_status = models.IntegerField(choices=APPROVE_STATUS_CHOICES, default=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
