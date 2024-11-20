from django.shortcuts import render, redirect,get_object_or_404
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
from .models import IdentificationNumber
from django.http import JsonResponse
from .forms import IdentificationNumberForm

@login_required
def home(request):
    
    
    return render(request,"home.html")


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





# # Create or Add identification_number Numbers
# def add_identification_numbers(request):
#     if request.method == 'POST':
#         # identification_numbers = request.POST.getlist('identification_numbers[]')  # Expecting a list from the frontend
#         identification_numbers = request.POST.getlist('identification_numbers[]')  # Expecting a list from the frontend
#         added = []
#         for identification_number in identification_numbers:
#             if not IdentificationNumber.objects.filter(identification_number=identification_number).exists():
#                 IdentificationNumber.objects.create(identification_number=identification_number)
#                 added.append(identification_number)
#                 messages.success(request,'Number added successfully')
#                 return redirect('retrieve_identification_numbers')
#         # return JsonResponse({'status': 'success', 'added': added})
#     return render(request, 'add_identification_numbers.html')



# Create or Add identification_number Numbers
def add_identification_numbers(request):
    if request.method == 'POST':
        # identification_numbers = request.POST.getlist('identification_numbers[]')  # Expecting a list from the frontend
        identification_number = request.POST.get('identification_numbers')  # Expecting a list from the frontend
        if not IdentificationNumber.objects.filter(identification_number=identification_number).exists():
            IdentificationNumber.objects.create(identification_number=identification_number)
            messages.success(request,'Number added successfully')
            return redirect('retrieve_identification_numbers')
        
        else:
             messages.warning(request,'Number already exists')
        # return JsonResponse({'status': 'success', 'added': added})
    return render(request, 'add_identification_numbers.html')


# Retrieve identification_number Numbers
def retrieve_identification_numbers(request):
    identification_numbers = IdentificationNumber.objects.all()
    return render(request, 'retrieve_identification_numbers.html', {'identification_numbers': identification_numbers})

# Update a identification_number Number
def update_identification_number(request, pk):
    identification_number = get_object_or_404(IdentificationNumber, pk=pk)
    if request.method == 'POST':
        new_number = request.POST['new_identification_number']
        check_exists = IdentificationNumber.objects.filter(identification_number=new_number).exists()
        if not check_exists:
            identification_number.identification_number = new_number
            identification_number.save()
            messages.success(request,'Number sucessfully updated')
            return redirect('retrieve_identification_numbers')
        else: 
            messages.warning(request,'Number exists already')
            # return redirect('update_identification_number')
    return render(request, 'update_identification_number.html', {'identification_number': identification_number})


# Delete a identification_number Number
def delete_identification_number(request, pk):
    identification_number = get_object_or_404(IdentificationNumber, pk=pk)
    identification_number.delete()
    messages.success(request,'Number deleted successfully')
    return redirect('retrieve_identification_numbers')




def access_page(request):
    if request.method == 'POST':
        form = IdentificationNumberForm(request.POST)
        if form.is_valid():
            identification_number = form.cleaned_data['identification_number']
            # Check if the matric number exists
            if IdentificationNumber.objects.filter(identification_number=identification_number).exists():
                # Grant access to the restricted page
                messages.success(request,'Number found, proceed with the registration')
                return redirect('register')
                # return render(request, 'registration/register.html', {'identification_number': identification_number})
            else:
                # Invalid matric number
                messages.error(request,'Invalid number')
                return render(request, 'registration/sign_up_access_page.html', {
                    'form': form,
                    'error': 'Invalid Admission Number / Staff ID. Please try again.'
                })
    else:
        form = IdentificationNumberForm()
    
    return render(request, 'registration/sign_up_access_page.html', {'form': form})

