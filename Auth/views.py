from django.shortcuts import render, redirect

from MyUtility import check_data_to_update
from .models import RalkzUser
from django.contrib import messages
from django.contrib.auth import authenticate, login as l, logout as l_out
from django.contrib.auth.decorators import login_required


def register(request):
    objs = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['full_name']
        phno = request.POST['phno']
        email = request.POST['email']
        address = request.POST['address']
        privacy_policy = request.POST.get('privacy_policy', 'off') == 'on'
        objs = {'username' : username,'full_name' : name,'phno' : phno,'email' : email,'address' : address, 'privacy_policy': request.POST.get('privacy_policy', 'off')}

        '''
            1 > if privacy_policy is not accepted, show message
            2 > verify username for specified pattern
            3 > validate phone number if not validated
            4 > validate mail id if not done
            5 > save to db
        '''
        if not privacy_policy:
            messages.warning(request, 'accept privacy policy')
        elif '@' in username or ' ' in username.strip():
            messages.warning(request, "don't use '@' and space in username")
            objs['username'] = ''
        elif not 5 < len(username) < 20:
            messages.warning(request, "length of username must be in between 5 and 20")
            objs['username'] = ''
        elif RalkzUser.objects.filter(username=username).exists():
            messages.warning(request, 'username already taken')
            objs['username'] = ''
        elif not 5 < len(password) < 20:
            messages.warning(request, "length of password must be in between 5 and 20")
        elif len([x in password for x in ['_','!','#','$','%','&','(',')','*','+',',','-','.',',','//']]) < 3:
            messages.warning(request, 'use atleast 2 special characters')
        elif len(phno) != 10:
            messages.warning(request, "enter valid mobile number")
            objs['phno'] = ''
        elif any(x not in email for x in ('@', '.com')):
            messages.warning(request, "enter valid mail address")
            objs['email'] = ''
        elif RalkzUser.objects.filter(email=email).exists():
            messages.warning(request, 'this email is already taken')
            objs['email'] = ''
        else:
            user = RalkzUser.objects.create_user(username=username, password=password, phone=phno, address=address,
                                           email=email, full_name=name, accept_privacy_policy=privacy_policy,pass_hist=password)
            user.save()
            messages.success(request,'registration completed')
            return redirect('/auth/login/')

    return render(request, 'register.html', {'data': objs})


def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username= username, password=password)
    if user is not None:
        l(request, user=user)
        messages.info(request, 'login successfull')
        return redirect('/')
    else:
        messages.info(request, 'invalid credentials')
        return redirect('/auth/login/')

@login_required
def logout(request):
    l_out(request)
    messages.warning(request, 'logged out safely')
    return redirect('/')

@login_required
def profile(request):
    userdata = RalkzUser.objects.filter(username=request.user.username)[0]
    if request.method == 'GET':
        return render(request, 'edit_profile.html', {'data': userdata})

    if 'show_password' in request.POST or '' in request.POST:
        return redirect('/auth/profile/')
    elif 'email_veify' in request.POST:
        return redirect('/auth/profile/')
    elif 'phone_veify' in request.POST:
        return redirect('/auth/profile/')
    else:
        '''
        it's a POST request to edit profile.
        1 > check if phone number and email verified.
        2 > change the details and save
        '''
        # todo: check if phone number and email verified.
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['full_name']
        phno = request.POST['phno']
        email = request.POST['email']
        address = request.POST['address']

        user = RalkzUser.objects.filter(username=request.user.username)[0]
        for data in check_data_to_update(userdata, username=username, password=password, full_name=name, phone=phno, email=email, address=address ):
            if data.get('username'):
                if '@' in username or ' ' in username.strip():
                    messages.warning(request, "don't use '@' and space in username")
                    return redirect('/auth/profile')
                elif not 5 < len(username) < 20:
                    messages.warning(request, "length of username must be in between 5 and 20")
                    return redirect('/auth/profile')
                elif RalkzUser.objects.filter(username=username).exists():
                    messages.warning(request, 'username already taken')
                    return redirect('/auth/profile')
                else:
                    user.username = username
                    messages.warning(request, 'username updated successfully')
            elif data.get('password'):
                if not 5 < len(password) < 20:
                    messages.warning(request, "length of password must be in between 5 and 20")
                    return redirect('/auth/profile')
                elif len([x in password for x in ['_','!','#','$','%','&','(',')','*','+',',','-','.',',','//']]) < 3:
                    messages.warning(request, 'use atleast 2 special characters')
                    return redirect('/auth/profile')
                else:
                    user.set_password(password)
                    user.pass_hist += '-\\\\-'+password
            elif data.get('name'):
                user.full_name=name
            elif data.get('phno'):
                if len(phno) != 10:
                    messages.warning(request, "enter valid mobile number")
                    return redirect('/auth/profile')
                else:
                    user.phone= phno
            elif data.get('email'):
                if any(x not in email for x in ('@', '.com')):
                    messages.warning(request, "enter valid mail address")
                    return redirect('/auth/profile')
                elif RalkzUser.objects.filter(email=email).exists():
                    messages.warning(request, 'this email is already taken')
                    return redirect('/auth/profile')
                else:
                    user.email= email
            elif data.get('address'):
                user.address= address
        messages.warning(request, 'user detailes updated successfully')
        user.save()
        l_out(request)
        return redirect('/auth/login')
