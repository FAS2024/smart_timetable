from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from .models import Teacher, Subject, TimeSlot,IdentificationNumber
import random  # We'll use this for a basic random timetable generation (you can replace it with AI/algorithmic logic later).
from .models import TimetableEntry
from .models import CustomUser
from django.http import JsonResponse
from .forms import IdentificationNumberForm,VerifyIdentificationNumberForm,UserRegistrationForm
from django.urls import reverse
from .authentication import IdentificationNumberBackend



@login_required
def admin_home(request):
    return render(request,"admin_home.html")


@login_required
def teacher_home(request):
    return render(request,"teacher_home.html")



@login_required
def student_home(request):
    return render(request,"student_home.html")


@login_required
def home(request):
    return render(request,"home.html")


def login_view(request):
    if request.method == 'POST':
        identification_number = request.POST.get('identification_number')
        password = request.POST.get('password')
        
        # Authenticate the user
        # user = authenticate(request, username=username, password=password)
        user = authenticate(request, identification_number=identification_number, password=password)
        
        if user is not None:
            login(request, user,backend='timetable_app.authentication.IdentificationNumberBackend')
            messages.success(request, f'Welcome, {user.get_full_name}')
            
            # Dynamically generate the URL based on role
            redirect_url = None
            if user.role == 'admin':
                redirect_url = reverse('admin_home')
            elif user.role == 'teacher':
                redirect_url = reverse('teacher_home')
            elif user.role == 'student':
                redirect_url = reverse('student_home')
            else:
                redirect_url = reverse('home')  # Default fallback

            return redirect(redirect_url)   
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect to the login page

    return render(request, 'registration/login.html')


def register(request):
    # Retrieve the identification number from the session
    identification_number = request.session.get('identification_number')

    if not identification_number:
        messages.error(request, "You must first verify your identification number.")
        return redirect('access_page')  # Redirect to identification verification page

    try:
        # Check if the identification number exists and is not used
        id_instance = IdentificationNumber.objects.get(number=identification_number, is_used=False)
    except IdentificationNumber.DoesNotExist:
        messages.error(request, "Invalid or already used identification number.")
        return redirect('access_page')  # Redirect if not valid

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Extract form data
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password1']

            # Create the CustomUser with the identification number as the username
            user = CustomUser.objects.create_user(
                identification_number=id_instance.number,
                role = id_instance.role,
                email=email,
                phone=phone,
                address=address,
                password=password
            )

            # Mark the identification number as used
            id_instance.is_used = True
            id_instance.save()

            # Log the user in
            # login(request, user)

            messages.success(request, f"You have successfully registered as {user.identification_number}")
            return redirect('login')  # Redirect to the login page or home page
    else:
        # Pre-populate the form with the identification number
        initial_data = {'identification_number': identification_number}
        form = UserRegistrationForm(initial=initial_data)

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




def add_identification_numbers(request):
    if request.method == 'POST':
        form = IdentificationNumberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Identification number added successfully')
                return redirect('retrieve_identification_numbers')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = IdentificationNumberForm()

    return render(request, 'add_identification_numbers.html', {'form': form})




# Retrieve identification_number Numbers
def retrieve_identification_numbers(request):
    
    identification_numbers = IdentificationNumber.objects.all()
    context =  {
        'identification_numbers': identification_numbers
    }
    return render(request, 'retrieve_identification_numbers.html',context)

 

# Update a identification_number Number
def update_identification_number(request, pk):
    identification_number = get_object_or_404(IdentificationNumber, pk=pk)
    if request.method == 'POST':
            form = IdentificationNumberForm(request.POST,instance=identification_number)
            if form.is_valid():
                try:
                    form.save()
                    # identification_number.is_used = False
                    # identification_number.save()
                    messages.success(request, 'Identification number updated successfully')
                    return redirect('retrieve_identification_numbers')
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")
            else:
                messages.error(request, 'Please correct the errors below.')

    else:
        form = IdentificationNumberForm(instance=identification_number)
    context = {
        'form':form
    }
    return render(request, 'update_identification_number.html', context)


# Delete a identification_number Number
def delete_identification_number(request, pk):
    identification_number = get_object_or_404(IdentificationNumber, pk=pk)
    identification_number.delete()
    messages.success(request,'Number deleted successfully')
    return redirect('retrieve_identification_numbers')



def access_page(request):
    """
    User enters identification number to be verified before proceeding to registration.
    """
    if request.method == 'POST':
        form = VerifyIdentificationNumberForm(request.POST)
        if form.is_valid():
            identification_number = form.cleaned_data['identification_number']
            try:
                id_instance = IdentificationNumber.objects.get(number=identification_number)
                
                if id_instance.is_used == False:
                    # Store the identification number in the session
                    request.session['identification_number'] = identification_number
                    messages.success(request, "Verification complete, you can proceed with the registration.")
                    return redirect('register')
                
                else:
                    messages.error(request, "Invalid or already used identification number! Please try again.")
                    return redirect('access_page')
                    
            except IdentificationNumber.DoesNotExist:
                messages.error(request, "Invalid or already used identification number! Please try again.")
                return redirect('access_page')
    else:
        form = VerifyIdentificationNumberForm()

    return render(request, 'registration/sign_up_access_page.html', {'form': form})



# def add_teacher(request):
#     return render(request,'add_teachers.html')

def view_teachers(request):
    teachers = CustomUser.objects.filter(role="teacher")
    context =  {
        'teachers': teachers
    }
    return render(request,'view_teachers.html',context)
    
# def edit_teacher(request):
#     return render(request,'edit_teachers.html')


# def delete_teacher(request):
#     return render(request,'view_teachers.html')






# def add_student(request):
#     return render(request,'add_teachers.html')

def view_students(request):
    students = CustomUser.objects.filter(role="student")
    context =  {
        'students': students
    }
    return render(request,'view_students.html',context)
    
# def edit_student(request):
#     return render(request,'edit_teachers.html')


# def delete_student(request):
#     return render(request,'view_teachers.html')


