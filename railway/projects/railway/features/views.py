from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.db import connection
from django.contrib import messages
from .models import Profile, Train, Route
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import datetime
from collections import defaultdict


# Create your views here.
def show(request):
    pass

def train(request):

    if request.method == 'POST':
        train_name = request.POST['train-name']
        train_name = train_name.replace('(', '')
        train_name = train_name.replace(')', '')
        train_id = int(train_name[-3:])
        train_name = train_name[:-3]
        train_name = train_name.replace('_', ' ')

        train = Train.objects.get(tr_id = train_id)
        routes = Route.objects.filter(train = train)
        
        d = defaultdict(list)

        for route in routes:
            d[route.stops_name].append(route.stops_name)
            d[route.stops_name].append(route.arrival_time)
            d[route.stops_name].append(route.departure_time)
        
        context = {
            'route' : dict(d),
        }
        for key, value in d.items():
            for item in value:
                print(f"Item type {type(item)}")
                print(f'Item is {item}')


        return render(request, 'features/show.html', context)
        
    
    train_list = ["Rocket_Express(101)", "Rocket_Express(102)"]

    context = {
        'trains': train_list
    }

    return render(request, 'features/train.html', context)

@login_required(login_url='login')
def edit(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        post_code = request.POST['post-code']

        if len(fname)==0 or len(lname) == 0:
            messages.info(request, "Name field is empty")
            return render(request, 'features/edit.html')
        if len(email) == 0:
            messages.info(request, "Email field is empty")
            return render(request, 'features/edit.html')
            

        user = User.objects.get(username = request.user.username)
        profile = Profile.objects.get(user=user)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        profile.address = address
        profile.post_code = post_code

        profile.save()
        user.save()

        return render(request, 'features/home.html')


    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user = user)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'features/edit.html', context)

def contact(request):
    return render(request, 'features/contact.html')

@login_required(login_url='login')
def profile(request, username):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    context = {
        'profile': profile,
        'user' : user
    }
    return render(request, 'features/profile.html', context)

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        source = request.POST['source']
        destination = request.POST['destination']
        doj = request.POST['doj']
        ticket_class = request.POST['ticket-class']
        time = datetime.datetime.now()
        print(time)

        print(doj)
        print(source)
        return render(request, 'features/home.html')

    station_list = ['Khulna', 'Jashore', 'Kotchadpur', 'Darshana', 'Chuadanga', 'Noapara', 'Mubarakganj', 'Alamdanga',
                    'Poradaha', 'Mirpur', 'Bheramara', 'Ishwardi', 'Chatmohar', 'Boral_Bridge', 'Ullapara', 'SHM Monsur Ali',
                    'BBSetu_E', 'Joydebpur', 'Biman_Bandar', 'Dhaka']
    class_list = ['SHOVAN', 'S_CHAIR', 'F_SEAT', 'SNIGDHA', 'AC_B', 'AC_S', 'SHULOV', 'AC_CHAIR', 'F_BERTH','F_CHAIR', ]
    station_list = sorted(station_list)
    class_list = sorted(class_list)
    return render(request, 'features/home.html', {'station_list': station_list, 'class_list': class_list})


        
def login(request):
    if request.method == 'POST':
        username = request.POST['phone']
        password = request.POST['password']
        
        query = """
                SELECT * 
                FROM auth_user 
                WHERE username = %s 
        """
        params = (username,)

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
        

        if row is not None:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                print("login successful")
                auth.login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Incorrect password')
                return redirect('login')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'features/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('first-name')
        lname = request.POST.get('last-name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm-password')
        nid = request.POST.get('nid')
        postcode = request.POST.get('post-code')

        if pass1 == pass2:
            if username and User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            elif email and User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif nid and Profile.objects.filter(nid=nid).exists():
                messages.info(request, 'NID already exists')
                return redirect('register')
            elif email and  Profile.objects.filter(phone=phone).exists():
                messages.info(request, 'Phone number already exists')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=pass1, first_name = fname, last_name = lname)
                user.save()

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, nid=nid, post_code=postcode, phone=phone)
                new_profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            redirect('register')

    else:
        return render(request, 'features/register.html')
'''
                query = """
                        INSERT INTO auth_user (username, email, password, first_name, last_name,is_superuser, is_staff,is_active, date_joined) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                params = (username, email, pass1, fname, lname, 0, False, False, datetime.datetime.now())

                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                
                query = """
                        SELECT id 
                        FROM auth_user 
                        WHERE username = %s 
                        """
                params = (username,)

                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    user_id = cursor.fetchone()[0]
                
                query = """
                        INSERT INTO Profile (user_id, nid, post_code, phone) 
                        VALUES (%s, %s, %s, %s)
                """
                params = (user_id, nid, postcode, phone)

                with connection.cursor() as cursor:
                    cursor.execute(query, params)
'''


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')