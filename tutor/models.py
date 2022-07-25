from django.db import models
from hod.models import batch
from student.models import profile_student
from django.utils import timezone


class leave_request(models.Model):
    student = models.ForeignKey(profile_student, on_delete=models.CASCADE)
    batch = models.ForeignKey(batch, on_delete=models.CASCADE)
    request = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=256, null=True, default="pending")
    requested_date = models.DateTimeField(default=timezone.now)
    approved_date = models.DateTimeField(null=True)

    def __str__(self):
        name = self.id
        return name
