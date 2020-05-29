from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup(request):
    if request.method =="POST":
        user_name = request.POST['user_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if request.POST['acctype'] == 'true':
            acctype = True
            is_staff = True
        else:
            acctype = False
            is_staff = False
        if password1 == password2:
            if User.objects.filter(username =user_name).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            
            elif User.objects.filter(email = email).exists():
                messages.info(request,'Email Exists')
                return redirect('signup')
            user = User.objects.create_user(username = user_name,email= email, password = password1, is_superuser = acctype, is_staff = is_staff)
            user.save()
            return redirect('signin')
        else:
            messages.info(request,'Wrong Password')
            return redirect('signup')
    else:
        return render(request,'user/signup.html')
def signin(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        user = auth.authenticate(username = username ,password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('Website-index')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('signin')
    return render(request,'user/signin.html')

def logout(request):
    auth.logout(request)
    return redirect('/')