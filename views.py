from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Litigant, Judge, Admin, Case,UserType
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .case import CaseForm  # Import CaseForm from your case.py file
from django.contrib import admin
from djangoapp.forms import UserRegistrationForm
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.test import TestCase



def homepage(request):
    return render(request, 'index.html')


def litigant_list(request):
    litigants = Litigant.objects.all().select_related()  # Use select_related to reduce database queries
    return render(request, 'litigant_list.html', {'litigants': litigants})

@login_required
def litigant_dashboard(request):
    judges = Judge.objects.all()  # Retrieve available judges

    # Retrieve cases associated with the logged-in litigant
    cases = Case.objects.all()

    return render(request, 'litigantdashboard.html', {
        'judges': judges,
        'cases': cases,
    })

def submit_case(request):
    if request.method == 'POST':
        case_number = request.POST['case_number']
        judge_id = request.POST['judge']
        status = request.POST['status']
        details = request.POST['details']
        
        # Assuming the litigant submitting the case is the logged-in user
        #litigant = request.user.litigant  # Adjust as necessary for your setup
        judge = Judge.objects.get(id=judge_id)
        
        Case.objects.create(
            case_number=case_number,
            judge=judge,
            status=status,
            details=details
        )
    
        messages.success(request, 'Your case has been submitted successfully.')
        return redirect('litigant_dashboard')
    
    return redirect('submit_case')  # Redirect if the form is not submitted via POST 


def drop_case(request):
    # Fetch all cases to display in the dropdown
    cases = Case.objects.all()

    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        case = get_object_or_404(Case, id=case_id)

        # Drop (delete) the case
        case.delete()

        messages.success(request, 'The case has been dropped successfully.')
        return redirect('litigant_dashboard')  # Redirect after dropping

    # Render the form with available cases if not a POST request
    return render(request, 'drop_case.html', {'cases': cases}) 


def case_file_list(request):
    cases = Case.objects.select_related('judge').all()  # Use select_related to fetch related judge data efficiently
    return render(request, 'CASE_FILE.html', {'cases': cases})


def judge_list(request):
    # Retrieve all judges and annotate each with the count of assigned cases
    judges = Judge.objects.annotate(case_count=Count('cases'))

    return render(request, 'judges.html', {'judges': judges})


def judge_case_list(request, judge_id):
    # Retrieve the judge and their cases
    judge = get_object_or_404(Judge, id=judge_id)
    cases = Case.objects.filter(judge=judge)
    return render(request, 'judge_case_list.html', {'judge': judge, 'cases': cases})

@login_required
def judge_dashboard(request):
    # Annotate each judge with the count of cases assigned to them
    judges = Judge.objects.annotate(case_count=Count('cases'))
    return render(request, 'judge_dashboard.html', {'judges': judges})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on roles
            if hasattr(user, 'judge'):
                return redirect('judge_dashboard')  # Adjust name if necessary
            elif hasattr(user, 'litigant'):
                return redirect('litigant_dashboard')  # Adjust name if necessary
            elif hasattr(user, 'admin'):  # Assuming admin is another model
                return redirect('admin_dashboard')  # Adjust name if necessary
            else:
                return redirect('homepage')  # Default fallback
            
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:  # Admin role
            return reverse('admin_dashboard')
        elif hasattr(user, 'judge'):  # Judge role
            return reverse('judge_dashboard')
        elif hasattr(user, 'litigant'):  # Litigant role
            return reverse('litigant_dashboard')
        else:
            return reverse('homepage') 

def RoleBasedLoginView(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'judge'):
            return redirect('judge_dashboard')  # Redirect for judges
        elif hasattr(request.user, 'litigant'):
            return redirect('litigant_dashboard')  # Redirect for litigants
        elif hasattr(request.user, 'admin'):
            return redirect('admin_dashboard')  # Redirect for admins
        else:
            return redirect('homepage')  # Default fallback
    else:
        return redirect('login')
    

@login_required
def admin_dashboard(request):
    return render(request, 'admindashboard.html')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            role = form.cleaned_data.get('role')
            name = request.POST.get('name')

            user = User.objects.create_user(username=username, email=email, password=password)
            userrole = UserType.objects.create(user=user, user_type=role)
            if role == 'litigant':
                Litigant.objects.create(user=user, name=name, email=email)
            elif role == 'judge':
                Judge.objects.create(user=user, name=name)
            elif role == 'admin':
                Admin.objects.create(user=user, name=name, email=email)

            messages.success(request, f'Account created successfully for {username}.')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

class ViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_litigant_dashboard_view(self):
        response = self.client.get(reverse('litigant_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'litigant_dashboard.html')

    def test_admin_dashboard_redirect_for_non_admin(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)  
