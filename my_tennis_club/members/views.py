import json
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404, render, redirect
import requests
from .forms import CustomAuthenticationForm
from my_tennis_club.settings import AUTH_USER_MODEL
from django.contrib.auth.decorators import login_required
from .models import User, Department
from .forms import NewTicketForm

def new_ticket(request):
    users = User.objects.all()
    user = request.user 
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            priority = form.cleaned_data['priority']
            email = user.email
            payload = """{"ticket": {"comment": { "body": "%s"   },"priority": "%s",    "subject": "%s"  }}"""
            payload = payload % (body, priority,subject)
            url = "https://bitsinfotec.zendesk.com/api/v2/tickets"
            payload = json.loads(payload)
            headers = {"Content-Type": "application/json", }
            response = requests.request("POST",	url, auth=(
                'anujshukla.shukla4@gmail.com', 'Anuj@shukla'), headers=headers, json=payload)
            message = "Ticket created successfully!"
            return render(request, 'ticket_confirmation.html', {'message': message})
    else:
        form = NewTicketForm()
    return render(request, 'new_ticket.html', {'form': form, 'users': users})

def manage_tickets(request):
    url = "https://bitsinfotec.zendesk.com/api/v2/tickets"
    headers = {	"Content-Type": "application/json",}
    response = requests.request("GET",	url,auth=('anujshukla.shukla4@gmail.com', 'Anuj@shukla'), headers=headers)
    response=json.loads(response.text)
    tickets = response['tickets']    
    return render(request, 'manage_tickets.html', {'tickets': tickets})


def delete_ticket(request, id):
    url = "https://bitsinfotec.zendesk.com/api/v2/tickets/%d"
    url = url % (int(id))
    headers = {	"Content-Type": "application/json",}
    response = requests.request("DELETE",url,auth=('anujshukla.shukla4@gmail.com', 'Anuj@shukla'), headers=headers)
    print(response.text)
    return redirect('manage_tickets')
#====================================================================================UserViews
def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        department_id = request.POST['department']
        role = request.POST['role']
        department = Department.objects.get(id=department_id)
        created_by = request.user
        User.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            password=password,
            department=department,
            role=role,
            created_by=created_by
        )
        return redirect('/user_list')
    else:
        departments = Department.objects.all()
        return render(request, 'create_user.html', {'departments': departments})

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users':users})



#============================================================================DepartmentViews

def assign_department(request):
    if request.method == 'POST':
        user_id = request.POST['user']
        department_id = request.POST['department']
        user = User.objects.get(id=user_id)
        department = Department.objects.get(id=department_id)
        user.department = department
        user.save()
        return redirect('user_list')
    else:
        users = User.objects.all()
        departments = Department.objects.all()
        return render(request, 'assign_department.html', {'users': users, 'departments': departments})
    
def create_department(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Department.objects.create(
            name=name,
            description=description
        )
        return redirect('/department_list')
    else:
        return render(request, 'create_department.html')

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html',{'departments': departments})

def update_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        department.name = request.POST['name']
        department.description = request.POST['description']
        department.save()
        return redirect('/department_list')
    else:
        return render(request, 'update_department.html', {'department': department})


def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if department.user_set.exists():
        error_message = "Department is associated with users and cannot be deleted."
        return render(request, 'department_list.html', {'departments': Department.objects.all(), 'error_message': error_message})
    else:
        department.delete()
        return redirect('/department_list')


#============================================================================login views
def login_view(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')
        user = authenticate(request, username=email_or_username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/homepage')
    return render(request, 'login.html')


def signup(request):
    error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cfm_password = request.POST.get('cfm_password')
        
        if password != cfm_password:
            error = "your password and confirm password are not same"
        else:
            my_user = AUTH_USER_MODEL(username, email , password)
            my_user.save()
            return redirect('login')
        print(error)
    return render(request , 'signup.html' , {"error":error})

def homepage(request):
    return render(request, 'homepage.html')

