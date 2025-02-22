from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


def register(request):
    if request.method == 'POST':
        # GET FORM VALUES
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # VALIDATIONS
        if password == password2:
             # USERNAME CHECK
            if User.objects.filter(username=username).exists(): # this is some shitty code, we need to find a way to defin this username property as unique in the db
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                # EMAIL CHECK
                if User.objects.filter(email=email).exists(): # this is some shitty code, we need to find a way to defin this username property as unique in the db
                    messages.error(request, 'Email is already taken')
                    return redirect('register')
                else:
                # VALIDATIONS PASSED
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    # Login after register
                    # auth.login(request, login) # you need to import auth from django.contrib
                    # messages.success(request, 'You are now logged-in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'User succesfully registered')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Succesfully logged out')
        return redirect('index')

