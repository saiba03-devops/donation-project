from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest
import razorpay
from .models import Contact

from .models import Donation
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'AboutUs.html')


def why_children(request):
    cards = [
        {
            'number': '33',
            'title': 'million',
            'description': 'child labourers go to work instead of school',
            'source': 'Census 2011'
        },
        {
            'number': '1 of 3',
            'title': 'child',
            'description': 'brides in the world is from India',
            'source': 'UNICEF 2014'
        },
        {
            'number': '2 of 3',
            'title': 'child',
            'description': 'deaths below the age of 5 are caused by malnutrition',
            'source': 'UNICEF 2019'
        },
    ]

    return render(request, 'whyChildren.html', {'cards': cards})


def child_education(request):
    return render(request, 'childEducation.html')


def child_health(request):
    return render(request, 'child-Health.html')


def stop_child_labour(request):
    return render(request, 'Stop-Child-labour.html')

def contact(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            location=location,
            subject=subject,
            message=message
        )

        send_mail(
            subject,
            f"""
Name: {name}
Email: {email}
Phone: {phone}
Location: {location}

Message:
{message}
            """,
            settings.EMAIL_HOST_USER,
            ['sahibamehtab2003@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")

        return redirect('contact')

    return render(request, 'Contact.html')

def faqs(request):
    return render(request, 'Faqs.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):

    donations = Donation.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_donations = donations.count()

    children_helped = total_donations * 2

    return render(request, 'dashboard.html', {
        'donations': donations,
        'total_donations': total_donations,
        'children_helped': children_helped,
    })


@login_required(login_url='login')
def donate(request):
    if request.method == "POST":
        citizenship = request.POST.get('citizenship') or "Indian Citizen"
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, "Please enter donation amount")
            return redirect('donate')

        amount = int(amount)

        fullname = request.POST.get('fullname')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pan = request.POST.get('pan')

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        payment = client.order.create({
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": 1
        })

        donation = Donation.objects.create(
            user=request.user,
            citizenship=citizenship,
            amount=amount,
            fullname=fullname,
            dob=dob,
            email=email,
            mobile=mobile,
            address=address,
            pincode=pincode,
            city=city,
            state=state,
            pan=pan,
            razorpay_order_id=payment['id'],
            payment_status="Pending"
        )

        return render(request, "payment.html", {
            "donation": donation,
            "payment": payment,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        })

    return render(request, 'donate.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            donation = Donation.objects.get(
                razorpay_order_id=razorpay_order_id
            )

            donation.razorpay_payment_id = razorpay_payment_id
            donation.razorpay_signature = razorpay_signature
            donation.payment_status = "Paid"
            donation.save()

            messages.success(request, "Payment successful")
            return redirect('dashboard')

        except Exception:
            return HttpResponseBadRequest("Payment verification failed")

    return HttpResponseBadRequest("Invalid request")