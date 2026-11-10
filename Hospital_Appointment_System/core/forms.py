from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Doctor, Appointment

class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = (field.widget.attrs.get("class", "") + " " + css).strip()

class RegisterForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

class DoctorForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["name", "specialty", "email", "phone", "consultation_fee", "available_days", "bio", "is_active"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

class AppointmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["doctor", "appointment_date", "appointment_time", "reason"]
        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time"}),
            "reason": forms.Textarea(attrs={"rows": 3, "placeholder": "Briefly describe the reason for your visit"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = Doctor.objects.filter(is_active=True)
        self.apply_bootstrap()
    def clean_appointment_date(self):
        value = self.cleaned_data["appointment_date"]
        if value < timezone.localdate():
            raise forms.ValidationError("Please choose today or a future date.")
        return value
