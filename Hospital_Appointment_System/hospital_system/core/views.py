from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm, DoctorForm, AppointmentForm
from .models import Doctor, Appointment

def home(request):
    return render(request, "core/home.html", {"doctor_count": Doctor.objects.filter(is_active=True).count()})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "core/form_page.html", {"form": form, "heading": "Create your account", "button": "Register"})

@login_required
def dashboard(request):
    if request.user.is_staff:
        appointments = Appointment.objects.select_related("patient", "doctor")
        context = {
            "total_appointments": appointments.count(),
            "pending": appointments.filter(status="Pending").count(),
            "confirmed": appointments.filter(status="Confirmed").count(),
            "doctor_count": Doctor.objects.count(),
            "recent": appointments[:6],
            "staff_view": True,
        }
    else:
        appointments = Appointment.objects.filter(patient=request.user).select_related("doctor")
        context = {
            "total_appointments": appointments.count(),
            "pending": appointments.filter(status="Pending").count(),
            "confirmed": appointments.filter(status="Confirmed").count(),
            "doctor_count": Doctor.objects.filter(is_active=True).count(),
            "recent": appointments[:6],
            "staff_view": False,
        }
    return render(request, "core/dashboard.html", context)

def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff)(view))

def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True)
    query = request.GET.get("q", "").strip()
    specialty = request.GET.get("specialty", "").strip()
    if query:
        doctors = doctors.filter(Q(name__icontains=query) | Q(specialty__icontains=query))
    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)
    specialties = Doctor.objects.filter(is_active=True).values_list("specialty", flat=True).distinct()
    return render(request, "core/doctor_list.html", {"doctors": doctors, "query": query, "specialties": specialties, "selected_specialty": specialty})

@staff_required
def doctor_create(request):
    form = DoctorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Doctor added successfully.")
        return redirect("doctor_list")
    return render(request, "core/form_page.html", {"form": form, "heading": "Add doctor", "button": "Save doctor"})

@staff_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorForm(request.POST or None, instance=doctor)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Doctor details updated.")
        return redirect("doctor_list")
    return render(request, "core/form_page.html", {"form": form, "heading": "Update doctor", "button": "Update doctor"})

@staff_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == "POST":
        doctor.is_active = False
        doctor.save()
        messages.success(request, "Doctor was deactivated.")
        return redirect("doctor_list")
    return render(request, "core/confirm_delete.html", {"object": doctor, "heading": "Deactivate doctor"})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related("doctor", "patient")
    if not request.user.is_staff:
        appointments = appointments.filter(patient=request.user)
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    if query:
        appointments = appointments.filter(Q(doctor__name__icontains=query) | Q(reason__icontains=query))
    if status:
        appointments = appointments.filter(status=status)
    return render(request, "core/appointment_list.html", {"appointments": appointments, "query": query, "selected_status": status})

@login_required
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        appointment = form.save(commit=False)
        appointment.patient = request.user
        try:
            appointment.save()
            messages.success(request, "Appointment request submitted.")
            return redirect("appointment_list")
        except IntegrityError:
            form.add_error(None, "That doctor’s time slot is already booked. Please select another time.")
    return render(request, "core/form_page.html", {"form": form, "heading": "Book an appointment", "button": "Submit appointment"})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if not request.user.is_staff and appointment.patient_id != request.user.id:
        messages.error(request, "You do not have permission to edit this appointment.")
        return redirect("appointment_list")
    if appointment.status in ["Completed", "Cancelled"]:
        messages.error(request, "Completed or cancelled appointments cannot be edited.")
        return redirect("appointment_list")
    form = AppointmentForm(request.POST or None, instance=appointment)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Appointment updated.")
            return redirect("appointment_list")
        except IntegrityError:
            form.add_error(None, "That doctor’s time slot is already booked.")
    return render(request, "core/form_page.html", {"form": form, "heading": "Edit appointment", "button": "Update appointment"})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if not request.user.is_staff and appointment.patient_id != request.user.id:
        messages.error(request, "You do not have permission to cancel this appointment.")
        return redirect("appointment_list")
    if request.method == "POST":
        appointment.status = "Cancelled"
        appointment.save()
        messages.success(request, "Appointment cancelled.")
        return redirect("appointment_list")
    return render(request, "core/confirm_delete.html", {"object": appointment, "heading": "Cancel appointment"})
