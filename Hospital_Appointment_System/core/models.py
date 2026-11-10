from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

class Doctor(models.Model):
    name = models.CharField(max_length=120)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    available_days = models.CharField(max_length=120, default="Monday - Friday")
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"Dr. {self.name} — {self.specialty}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"), ("Confirmed", "Confirmed"),
        ("Completed", "Completed"), ("Cancelled", "Cancelled"),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="appointments")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]
        constraints = [
            models.UniqueConstraint(fields=["doctor", "appointment_date", "appointment_time"],
                                    condition=~models.Q(status="Cancelled"),
                                    name="unique_active_doctor_slot")
        ]

    def __str__(self):
        return f"{self.patient.username} - {self.doctor} - {self.appointment_date}"
