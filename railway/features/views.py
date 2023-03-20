from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.db import connection
from django.contrib import messages
from .models import Profile, Train, Route, Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import datetime
from collections import defaultdict
from reportlab.pdfgen import canvas


# Create your views here.

def generatepdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 750, 'Ticket-details')
    p.drawString(100, 700, f"Train ID: {request.session.get('tr-id')}")
    p.drawString(100, 650, f"Train: {'gh'}")
    p.drawString(100, 600, f"From: {request.session.get('source')}")
    p.drawString(100, 550, f"To: {request.session.get('destination')}")
    p.drawString(100, 500, f"Date: {request.session.get('doj')}")
    p.drawString(100, 450, f"Passenger Name: {request.user.first_name} {request.user.last_name}")
    p.drawString(100, 400, f"Number of Passengers: {'1'}")
    p.showPage()
    p.save()
    return response

def booking(request, name):
    if request.method == 'GET':
        seat = request.GET['seat-no']
        print(seat)
        pdf_response = generatepdf(request)
        return pdf_response
    
    else:

        source  = request.session.get('source')
        destination = request.session.get('destination')
        doj = request.session.get('doj')
        request.session['tr-id']  = name
        print(doj)
        print(name)
        rows = ""
        tr = Train.objects.get(tr_id = name)
        print(tr)
        bookings = Booking.objects.filter(train=tr, booking_date = doj)
        
        booked = []
        if bookings.exists():
            rows = bookings.all()

        
        for row in rows:
            booked.append(row.seat_number)
        print(booked)
        available_seat = []
        for i in range(1, 101):
            if i in booked:
                pass
            else :
                available_seat.append(i)
        

        '''
        query  = """
            SELECT B.seat_number
            FROM Booking as B
            WHERE B.train = %s and booking_date = %s
        """
        params = (train,  doj)
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        
        for row in rows:
            print(row)
        '''
        '''
        query  = """
                SELECT R.serial_no
                FROM Route as R
                WHERE R.stops_name = %s
        """
        params = (source,  )
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
        
        request.session['from_id'] = row[0]
        print(row[0])

        query  = """
            SELECT R.serial_no
            FROM Route as R
            WHERE R.stops_name = %s
        """
        params = (destination,  )
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
    
        request.session['to_id'] = row[0]

        print(row[0])
        '''
        context = {
            'source' : source,
            'destination' : destination,
            'doj': doj,
            'seats': available_seat
        }



        return render(request, 'features/booking.html', context)

def available_train(request):
    return render(request, 'features/available_train.html')

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
            'route' : dict(d)
        }
        print(type(context))

        return render(request, 'features/show.html', context)
    
    train_list = ["Rocket_Express(101)", "Rocket_Express(102)", "Sagardari_Express(201)","Sagardari_Express(202)" ]

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
        time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().date()

        
        print(source)
        print(destination)
        request.session['source'] = source
        request.session['destination'] = destination
        request.session['doj'] = doj


        query = """
                SELECT T.tr_id
                from Train as T
                join Route as t1 on t1.stops_name = %s 
                join Route as t2 on t2.stops_name = %s 
                where t1.serial_no < t2.serial_no
        """
        params = (source, destination)
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchone()

        if rows is None:
            print("sorry there is no train available")
            return render(request, 'features/home.html')
        
        d = defaultdict(list)
        l = []
        for row in rows:
            l.append(str(row))
            query = """
                    SELECT R.departure_time
                    from Route as R
                    join Train as T on T.tr_id = %s and R.stops_name = %s
            """
            params = (row, source)

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                row2 = cursor.fetchone()
            print(row2[0])
            

            query = """
                    SELECT R.arrival_time
                    from Route as R
                    join Train as T on T.tr_id = %s and R.stops_name = %s
            """

            params = (row, destination)
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                row3 = cursor.fetchone()

            query = """
                    SELECT T.tr_name
                    from Train as T
                    where tr_id = %s
            """

            params = (row, )
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                row4 = cursor.fetchone()

            d[row4[0]].append(row2[0])
            d[row4[0]].append(row3[0])
            print(d)

            context = {
                'trains' : dict(d),
                'to' : destination,
                'from': source,
                'tr_id': l
            }


            return render(request, 'features/available_train.html', context)

    station_list = ['Khulna', 'Jashore', 'Kotchandpur', 'Darshana', 'Chuadanga', 'Noapara', 'Mubarakganj', 'Alamdanga',
                    'Poradaha', 'Mirpur', 'Bheramara', 'Ishwardi', 'Chatmohar', 'Boral_Bridge', 'Ullapara', 'SHM Monsur Ali',
                    'BBSetu_E', 'Joydebpur', 'Biman_Bandar', 'Dhaka']
    class_list = ['SHOVAN', 'S_CHAIR', 'F_SEAT', 'SNIGDHA', 'AC_B', 'AC_S', 'SHULOV', 'AC_CHAIR', 'F_BERTH','F_CHAIR', ]
    station_list = sorted(station_list)
    class_list = sorted(class_list)
    return render(request, 'features/home.html', {'station_list': station_list, 'class_list': class_list})


        
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
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
        
        print(row)
        print(username)

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