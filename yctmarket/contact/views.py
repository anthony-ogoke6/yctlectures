from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .forms import contactForm

# Create your views here.
def contact_page(request):
	title = 'Contact Us'
	form = contactForm(request.POST or None)
	confirm_message = None

	if form.is_valid():
	    email = form.cleaned_data['email']
	    phone_number = form.cleaned_data['phoneNumber']
	    name = form.cleaned_data['name']
	    comment = form.cleaned_data['comment']
	    subject = 'message from YCT-Market.com'
	    message = '%s %s %s %s' %(comment, name, email, phone_number)
	    emailFrom = form.cleaned_data['email']
	    emailTo = [settings.EMAIL_HOST_USER]
	    send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
	    title = 'Thanks'
	    confirm_message = 'Thanks for the message. We will get back to you shortly.'
	    form = None

	context = {'title': title, 'form': form, 'confirm_message': confirm_message,}
	template = 'contact/contact.html'
	return render(request,template,context)