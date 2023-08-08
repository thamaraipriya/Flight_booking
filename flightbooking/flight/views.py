from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from validate_email import validate_email
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import uuid

# Create your views here
def index(request):
    return render(request,'index.html')


def search(request):
    if request.method=="POST":
        From=request.POST['search_from']
        To=request.POST['search_to']
        date=request.POST['date']
        if From != To:
            if Flight_detail.objects.filter(Origin=From,Destination=To,Origin_date=date).exists():
                return HttpResponse('<h1><center>Yes Flight ticket is available<br>Go to Flight Reservation in home page</center></h1>')
            else:
                return HttpResponse('<h1><center>Flight ticket is not available.</center></h1>')
        else:
            return HttpResponse('<h1><center>Origin and Destination should not be same</center></h1>')

    else:
        return render(request,'search.html')

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if len(password)<7:
            messages.info(request,'Password should be atleast 8 characters')
            return redirect('register')
        if not validate_email(email):
            messages.info(request,'Enter valid Email')
            return redirect('register')
        if not username:
            messages.info(request,'Username is required!')
            return redirect('register')
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email-id already exist!')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exist!')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.set_password(password)
                user.save()
                auth_token=str(uuid.uuid4())
                profile_obj=Profile.objects.create(user=user,auth_token=auth_token)
                profile_obj.save()
                send_mail_after_reg(email,auth_token)
                return redirect('token')
        else:
            messages.info(request,'Password doesnot match')
            return redirect('register')
    else:
        return render(request,'register.html')
    
def mybooking(request):
    booking=User_booking.objects.all()
    return render(request,'mybooking.html',{'booking':booking})

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
    
def booking(request):
    if request.method=='POST':
        booking=User_booking()
        booking.Origin=request.POST.get('from')
        booking.Destination=request.POST.get('to')
        booking.Preferred_Seating=request.POST.get('pre_seat')
        booking.Departure_date=request.POST.get('Text')
        booking.Adult=request.POST.get('adult')
        booking.Child=request.POST.get('child')
        booking.Infant=request.POST.get('infant')
        booking.Return_date=request.POST.get('Text1')
        booking.Full_name=request.POST.get('fullname')
        booking.Email=request.POST.get('email')
        booking.Mobile_number=request.POST.get('mobileno')
        booking.save()
        messages.info(request,'Your Flight ticket is reserved')
        return redirect('index')
    else:
        return render(request,'booking.html')
   

def token(request):
    return render(request,'token.html')

def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).exists()
        if profile_obj:
            if profile_obj.is_verified:
                return HttpResponse("<h1><center>Your account has been already verified</center></h1>")
            profile_obj.is_verified=True
            profile_obj.save()
            return HttpResponse("<h1><center>Your account is verified Successfully</center></h1>")
        else:
            messages.info(request,'Error')
            return redirect('login')
    except Exception as e:
        return redirect('login')  

def logout(request):
    auth.logout(request)
    return redirect('/')

def send_mail_after_reg(email, token):
    subject='Your account need to be verified'
    message=f'Link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)