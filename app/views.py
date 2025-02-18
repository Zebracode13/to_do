from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Task
from .forms import TaskForm, UserCreateForm,ContactForm
from django.core.mail import send_mail

def about(request):
    contact_form = ContactForm()  # Ensure a form instance is created

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']

            # Send an email (Make sure email settings are configured in settings.py)
            send_mail(
                f'Contact Form Submission from {name}', 
                message,
                email,
                ['your_email@example.com'],  # Replace with your email
                fail_silently=False,
            )

            return redirect('about')  # Redirect to prevent multiple submissions

    return render(request, 'about.html', {'contact_form': contact_form})  # Pass form instance to the template


def about(request):
    return render(request, 'about.html')

class SignupView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        form = UserCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome!")
            return redirect('home')  # Redirect to home after successful signup
        messages.error(request, "Signup failed. Please correct the errors below.")
        return render(request, self.template_name, {'form': form})

# HomePage View - Handles Task Display and Task Management
class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(owner=self.request.user)
        context["task_form"] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, "Task added successfully!")
        else:
            messages.error(request, "Failed to add task. Please check the input fields.")
        return redirect('home')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if not task.completed:
        task.completed = True
        task.completed_date = timezone.now()  # Store the completion date and time
        task.save()
        messages.success(request, f"Task '{task.title}' marked as completed!")
    return redirect('home')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.delete()
    messages.warning(request, "Task deleted successfully!")
    return redirect('home')


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == "POST":
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            messages.info(request, "Task updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "Failed to update task. Please check the input fields.")
    else:
        task_form = TaskForm(instance=task)
    
    return render(request, "update_task.html", {
        "form": task_form,  # Updated to match frontend template
        "task": task
    })


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully!")
    return redirect('login')  # Redirect user to login page after logout
