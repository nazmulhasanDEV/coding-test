from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login')
def home(request):

    users = User.objects.all()

    context = {
        'users': users
    }

    return render(request, 'home.html', context)


def registration(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmpass = request.POST['con_pass']
        type = request.POST['type']


        if name and email and username and password and confirmpass:
            if  len(User.objects.filter(email=email)) <= 0 and len(User.objects.filter(username=username)) <= 0:
                if password == confirmpass:
                    try:
                        if type == 'admin':
                            user_account = User.objects.create_superuser(email=email, username=username, password=password)
                            user_account.first_name = name
                            user_account.save()

                            # # sending verification email with code*********************************

                            # subject = f"Verification Link"
                            # verification_url = f"Click to verify account: http://127.0.0.1:8000/user/account/veirfication/{username}/{phone}/"
                            # html_content = render_to_string('backEnd_superAdmin/verification_template.html',
                            #                                 context={'verification_url': verification_url})
                            # email = EmailMessage(subject, html_content, to=[email])
                            # email.content_subtype = 'html'
                            # EmailThreading(email).start()
                            # messages.success(request, "Verification link sent to your email!")
                            messages.success(request, "Account has been created successfully!")
                            return redirect('registration')
                        else:
                            user_account = User.objects.create_user(email=email, username=username,
                                                                         password=password)
                            user_account.first_name = name
                            user_account.save()
                            messages.success(request, "Account has been created successfully!")
                            return redirect('registration')
                    except:
                        messages.warning(request, "Can't create account! Try again!")
                        return redirect('registration')
                    # ends sending verification email with code*************************

                else:
                    messages.warning(request, "Password didn't match! Try again!")
                    return redirect('registration')
            else:
                messages.warning(request, "User already exists!")
                return redirect('registration')

    return render(request, 'registration.html')


def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)


        if username and password:
            try:
                user = get_object_or_404(User, username=username)
                try:
                    if user and user.is_active == True:
                        authenticate_user = authenticate(request, username=username, password=password)
                        print(authenticate_user)
                        if authenticate_user:
                            login(request, authenticate_user)
                            return redirect('home')
                        else:
                            messages.warning(request, "You are not authenticated yet!")
                            return redirect('login')
                    else:
                        messages.warning(request, "Please verify your account to acccess!")
                        return redirect('login')
                except:
                    messages.warning(request, "User not found!")
                    return redirect('login')
            except:
                messages.warning(request, 'Wrong username or email')
                return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('login')
