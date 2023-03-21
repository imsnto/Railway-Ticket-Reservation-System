from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.db import connection
from django.contrib import messages
from .models import Profile, Train, Route, Booking, TicketCost
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import datetime
from collections import defaultdict
from reportlab.pdfgen import canvas
import base64

# Create your views here.
def success(request):
    pdf_content_base64 = request.session['pdf_content_base64']
    pdf_content = base64.b64decode(pdf_content_base64)
    pdf_response = HttpResponse(pdf_content, content_type='application/pdf')
    pdf_response['Content-Disposition'] = 'attachment; filename="file.pdf"'

    context = {
        'pdf': pdf_content_base64,
    }
    return render(request, 'features/pdf.html', context)

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

def generatepdf(request):
    # Create a landscape PDF with letter size paper
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
    p = canvas.Canvas(response, pagesize=landscape(letter))

    # Set the font size and style
    p.setFont('Helvetica-Bold', 20)
    
    # Add a title
    p.drawCentredString(400, 580, 'Train Ticket')

    # Add a separator line
    p.line(100, 560, 700, 560)

    # Set the font size and style
    p.setFont('Helvetica', 14)

    # Add the passenger's name
    p.drawString(100, 520, 'Passenger Name:')
    p.drawString(250, 520, f'{request.user.first_name} {request.user.last_name}')

    # Add the phone number
    p.drawString(100, 480, 'Phone:')
    p.drawString(250, 480, f'{request.session.get("phone")}')

    # Add the NID number
    p.drawString(100, 440, 'NID:')
    p.drawString(250, 440, f'{request.session.get("nid")}')

    # Add the source and destination
    p.drawString(100, 400, 'Source:')
    p.drawString(250, 400, f'{request.session.get("source")}')
    p.drawString(100, 360, 'Destination:')
    p.drawString(250, 360, f'{request.session.get("destination")}')

    # Add the train name and seat number
    p.drawString(100, 320, 'Train Name:')
    p.drawString(250, 320, f'{request.session.get("train")}')
    p.drawString(100, 280, 'Seat Number:')
    p.drawString(250, 280, f'{request.session.get("seat")}')

    # Add the number of passengers
    p.drawString(100, 240, 'No. of Passengers:')
    p.drawString(250, 240, '1')

    p.drawString(100, 200, 'Date of Journey:')
    p.drawString(250, 200, f'{request.session.get("doj")}') 

    p.drawString(100, 160, 'Ticket Class:')
    p.drawString(250, 160, f'{request.session.get("class")}') 

    p.drawString(100, 120, 'Ticket Cost:')
    p.drawString(250, 120, f'{request.session.get("cost")}') 

    # Add a separator line
    p.line(100, 80, 700, 80)

    # Add a footer
    p.setFont('Helvetica', 10)
    p.drawCentredString(400, 20, 'Thank you for traveling with us!')

    # Save the PDF and return the response
    p.showPage()
    p.save()
    return response

def booking(request, name):
    if request.method == 'GET':
        seat = int(request.GET['seat-no'])
        source = request.session.get('source')
        destination = request.session.get('destination')
        doj = request.session.get('doj')
        tr_id = request.session.get('tr-id')
        f_name = request.user.first_name
        l_name = request.user.last_name


        user = User.objects.get(username = request.user.username)
        profile = Profile.objects.get(user=user)
        phone_number = profile.phone
        nid = profile.nid

        


        train = Train.objects.get(tr_id=tr_id)
        train_id = train.tr_id
        tr_name = train.tr_name
        class_seat = request.session.get('class')

        request.session['train'] = tr_name
        request.session['nid'] = nid
        request.session['phone'] = phone_number
        request.session['seat'] = seat


        query = """
                INSERT INTO Booking(train_id, seat_number, booking_date) VALUES(%s, %s, %s)
        """
        params = (train_id, seat, doj)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        query = """
                SELECT T.cost
                FROM TicketCost as T
                WHERE T.source=%s AND T.destination=%s
        """

        params = (source, destination)

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
        
        print("price")
        print(row)

        cost = 0
        if row is not None:
            cost = row[0]

        request.session['cost'] = cost

        pdf_response = generatepdf(request)
        pdf_content_base64 = base64.b64encode(pdf_response.content).decode('utf-8')
        request.session['pdf_content_base64'] = pdf_content_base64
        context = {
            'source' : source,
            'destination' : destination,
            'doj': doj,
            'tr_id': tr_id,
            'seat': seat,
            'train_name': tr_name,
            'phone': phone_number,
            'nid':nid, 
            'f_name': f_name,
            'l_name':l_name,
            'cost':cost,
            'class':class_seat
        }
        return render(request, 'features/success.html', context)
    
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
        request.session['class'] = ticket_class


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