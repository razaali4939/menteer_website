from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

def register_view(request):
    form = CreateUserForm()
    if request.method =='POST':
        
    #return render(request, "page-register.html")
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                # username = form.cleaned_data.get('username')
                # messages.success(request, 'Account was created for ' + username)
                #return redirect('login')
                userObj = form.cleaned_data
                username = userObj['username']
                email =  userObj['email']
                password =  userObj['password1']
                username = userObj.get('username')
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
    context={'form': form}
    return render(request, "register.html", context) #page-register

def login_view(request):    
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        print(username + ': I am username and ' + password + ': I am password')
        user = authenticate(request, username=username, password=password)
        print(str(request) + ' is the Request')
        if user is not None:
            print("I see am")
            login(request, user)
            return redirect('user_profile')
        else:
            messages.info(request, 'UserName Or Password is Incorrect')
            return render(request, "page-login.html")
    context={}
    return render(request, "page-login.html", context)

def home_view(request):
    return HttpResponse('Hey')
