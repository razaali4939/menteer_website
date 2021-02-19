from django.shortcuts import redirect,render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from .models import MyUser
from django.contrib.sites.shortcuts import get_current_site
import json,os
from django.http import HttpResponse,Http404,FileResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
import uuid
from django.views.generic.edit import FormView
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# from django.utils.http import (
#     url_has_allowed_host_and_scheme, urlsafe_base64_decode,
# )
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordContextMixin
import re
from .utils import generate_token
#from .token import account_activation_token
from django.utils.encoding import force_bytes, force_str, force_text
from django.template.loader import render_to_string
from validate_email import validate_email
from menteeor import settings
from django.core.mail import send_mail
#mail_send_from="menteeorapp@gmail.com"
#mail_send_from="django_appointments@deligence.com"
#mail_send_from="tehseenarshad227227@gmail.com"
UserModel = get_user_model()
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
# Create your views here.
def manage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():  
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None: 
                obj=MyUser.objects.get(email=email)
                if obj.is_active:
                    print(obj.role)
                    if obj.role == 'mentee':
                        login(request, user)
                        return redirect(f'/mentee/{obj.id}/')
                    if obj.role == 'mentor':
                        login(request, user)
                        return redirect(f'/mentor/{obj.id}/')
                    else:
                        return redirect('/notfound/')
                else:
                    messages.error(request, "Confirm your Email-Id first")
            else:
                messages.error(request, "Invalid Email-Id or password.")
        else:
            messages.error(request, "Invalid Email-Id or password.")
    form = AuthenticationForm()
    return render(request=request,template_name="auth/login.html", context={"form": form,'title':'Login'})
@login_required(login_url='/login/')
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/login/')
class RegistrationView(View):
    def get(self, request):
        #return redirect(request, 'register')
        return render(request, 'auth/register.html')

    def post(self, request):
        context = {

            'data': request.POST,
            'has_error': False
        }

        #if request.method == 'POST':
        email=request.POST.get('email')
        username = request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('confirmPassword')
        firstName=request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        city = request.POST.get('city')
        dob = request.POST.get('dob')
        gender = request.POST.get('customRadio1')
        country = request.POST.get('country')
        role = request.POST.get('role')
        state = request.POST.get('state')
        maritalStatus = request.POST.get('maritalStatus')
        age = request.POST.get('age')

        #validation can start here 
        if password != password2:
            messages.add_message(request, messages.ERROR,'passwords dont match') 
            context['has_error'] = True
        
        if not validate_email(email):
            messages.add_message(request, messages.ERROR,'Please provide a valid email')
            context['has_error'] = True

        try:
            if MyUser.objects.get(email=email):
           # if accounts_myuser.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is already register')
                context['has_error'] = True
        except Exception as identifier:
            pass


        try:
            if MyUser.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'Username is already register')
                context['has_error'] = True
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'auth/register.html', context, status=400)

        id=uuid.uuid4()
        user=MyUser.objects.create(id=id, email=email,role=role,is_active=False, fname=firstName, lname=lastName, country=country, city=city, state=state,
                                   maritalStatus=maritalStatus, age=age, gender=gender, date_of_birth=dob)
        user.set_password(password)
        user.is_active = False
        user.save()
        
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link=reverse('activate', kwargs={'uidb64':uidb64,'token':generate_token.make_token(user)})
        activate_url='http://'+ domain + link



        email_body=f'Hi, please activate your menteeor account with this linkn {activate_url}'
        email_subject='ACTIVATE YOUR MENTEEOR ACCOUNT'
        from_mail = settings.EMAIL_HOST_USER
        try:
            send_mail(email_subject, email_body, from_mail, [email], fail_silently=False)
            return render(request, 'auth/SignupConfirmation.html', {'email':email})
        except SMTPException as e:
            print('na the error be this', f'error  : {e}')
            #message = e
            #message = "Mail could not be sent, Please contact administrator"
            messages.add_message(request, messages.ERROR, 'Mail could not be sent, Please contact administrator')
            context['has_error'] = True
            return render(request,'auth/register.html')
        #return HttpResponse("<h1>Thank you for signing up!. We have Sent you a co</h1>")
        #return render(request, 'auth/SignupConfirmation.html', {'email':email})
class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):        
        try:
            uid = force_text(urlsafe_base64_decode(uidb64)) 
            user = MyUser.objects.get(pk=uid)
            print('Here are the creds:', uid, user)  
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
            #return render(request, 'auth/login.html')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')
            #return render(request, 'auth/login.html')
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR,
                                'Username is required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                'Password is required')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password)
        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login')
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'auth/login.html', status=401, context=context)
        login(request, user)
        return redirect('home')
@csrf_exempt

def showindex(request):
    return render(request, 'profile.html')
def check_username(request):
    if request.is_ajax():
        email=request.POST.get('username')
        obj=MyUser.objects.filter(email=email)
        if obj:
            return HttpResponse(json.dumps({'status': 'exists'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': 'available'}), content_type="application/json")
def password_reset(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save(from_email='django_appointments@appointments.com',request=request)
            messages.success(request, "link sent")
            return redirect('/accounts/login/')
        else:
            return HttpResponse("Invalid Request")
    else:
        form=PasswordResetForm()
        return render(request,'password_reset_form.html',{'form': form,'title':'Password Reset'})
def pass_changed_success(request):
    messages.success(request, "changed")
    return redirect('/accounts/login/')
class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('changed')
    template_name = 'password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
         form.save()
        #user = form.save()
        #del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
       # if self.post_reset_login:
         #   auth_login(self.request, user, self.post_reset_login_backend)
       # return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context

