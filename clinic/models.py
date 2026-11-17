from django.db import models

class Appointment(models.Model):
    patient_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    service = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100, default='Any Available Dentist')
    date = models.DateField()
    time_slot = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50, default='Pay at Clinic')
    payment_status = models.CharField(max_length=30, default='Pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.date} ({self.payment_method})"
