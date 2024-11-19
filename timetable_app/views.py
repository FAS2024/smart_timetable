from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

from .models import Teacher, Subject, TimeSlot
import random  # We'll use this for a basic random timetable generation (you can replace it with AI/algorithmic logic later).

from .models import TimetableEntry

from .forms import RegistrationForm

@login_required
def home(request):
    
    
    return render(request,"home.html")


# # Login View
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('generate_timetable')  # Redirect to the timetable generation page or home page
#         else:
#             messages.error(request, 'Invalid username or password.')
    
#     return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect to the login page

    return render(request, 'registration/login.html')




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Log the user in
            login(request, user)

            # Success message
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')  # Redirect to homepage or any page after successful registration
        else:
            # Handle form errors
            messages.error(request, "There was an error in the form.")
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def view_timetable(request):
    """
    A view to display the user's timetable.
    """
    # Fetch user's timetable or any other data you need to display
    # For now, we'll just display a placeholder message.
    return render(request, 'view_timetable.html')




@login_required
def update_timetable(request):
    """
    A view to update the user's timetable.
    """
    if request.method == 'POST':
        # Handle form submission for updating timetable
        # Example: Update timetable entries, etc.
        # You can update timetable logic here.
        return redirect('view_timetable')  # Redirect to the 'view_timetable' page after update

    # If the request is GET, render the timetable update form
    # Get current timetable entries for display in the form
    timetable_entries = TimetableEntry.objects.filter(user=request.user)  # Assuming user-specific timetable
    return render(request, 'update_timetable.html', {'timetable_entries': timetable_entries})




@csrf_protect
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')  # Redirect to login page


