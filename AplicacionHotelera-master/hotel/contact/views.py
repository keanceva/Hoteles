from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from contact.models import Suscriber
from django.contrib import messages

# Create your views here.


def contact(request):
    return render(request, 'contact_page.html')


def send_email(request):
    if request.method == 'POST':
        print("Entra a post")
        json_post = request.POST

        subject = json_post['subject']
        message = json_post['message']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['emiliojmp9@gmail.com', ]
        send_mail(subject, message, email_from, recipient_list)

    return redirect('/contact/')

def to_suscribe(request):    
    if request.method == 'POST':
        json_post = request.POST
        print(json_post)
        subcriber = Suscriber(
            email = json_post['email']
        )

        subcriber.save()
    
        messages.info(request, 'Se ha suscrito con éxito.')

        return redirect('/reservas/')
    else:
        return redirect('/reservas/')