from email.message import EmailMessage
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Cancer
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from project import settings
from django.core.mail import send_mail

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token


# Create your views here.
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        gender = request.POST['gender']
        calender = request.POST['calender']
        dateofbirth = request.POST['date-of-birth']
        dateoftime = request.POST['date-of-time']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')

        myuser = User.objects.create_user(username=username,email=email,password=pass1)
        cancer = Cancer.objects.create(username=username,gender=gender,calender=calender,dateofbirth=dateofbirth,dateoftime=dateoftime,email=email,pass1=pass1,pass2=pass2)

        myuser.save()
        cancer.save()

        messages.success(request,'your acount has been successfully created....! check your email for confirmation')
           # wel-come email
        subject = "Welcome to chatfate Login!!"
        message = "Hello..." + myuser.username + " \n" + "Welcome to chatfate!! \nthis is the confirmation email for chatfate regestration,\n please confirm your email address.\nThank you for Regestration \n\nThanking You\nAdmin"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # email confirmation link

        # current_site = get_current_site(request)
        # email_subject = "Confirm your Email @ Student - Portal!!"
        # message2 = render_to_string('email_confirmation.html',{
            
        #     'name': myuser.username,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token': generate_token.make_token(myuser)
        # })
        # email = EmailMessage(
        # email_subject,
        # message2,
        # settings.EMAIL_HOST_USER,
        # [myuser.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect('signin')

    return render(request,'signup.html')
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)

            messages.success(request, "Logged In Sucessfully!!")
            return render(request, "home.html")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')

    return render(request,'signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signup')