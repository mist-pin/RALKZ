from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from Home.models import Aspirants, Project
from Auth.models import RalkzUser


def home(request):
    return render(request, 'home.html')


def faq(request):
    return render(request, 'faq.html')


def career(request):
    '''
        check if the user is an employee or aspirant or customer or Anonymous user and add the details to the render context
    '''
    user = get_user(request)
    data = {}
    if user.is_authenticated:
        if user.is_employee:
            return redirect('/emp/')
        elif user.is_aspirant:
            db= Aspirants.objects.filter(user=user)
            data['application_status'] = db[0].application_status
    return render(request, 'career.html', {'data':data})


@login_required
def apply_job(request):
    user = get_user(request)

    if user.is_employee:
        messages.warning(request, 'You are already an employee')
        return redirect('/career/')

    data = {'form':True,'is_aspirant':user.is_aspirant}
    if Aspirants.objects.exists():
        db = Aspirants.objects.filter(user=user.username)[0]
        data['application_status']=db[0].application_status


    if request.method == "POST":
        resume = request.POST.get('resume',False)
        identity = request.POST.get('identity',False)
        experience = request.POST.get('experience',False)
        study = request.POST.get('study',False)
        if not any([resume, identity, study]):
            messages.warning(request, 'all fields excluding work experience proof are mandatory')
            return redirect('/career/apply/')
        else:
            db = Aspirants(user=user, resume=resume, identity_proof=identity, study_certificate=study)
            if  experience:
                Aspirants.experience_proof=experience
            db.save()
            user.is_aspirant = True
            user.save()
            messages.info(request, 'Application submitted')
            return redirect('/career/')

    return render(request, 'career.html', {'data':data})


def services(request):
    return render(request, 'services.html',)


def about(request):
    return render(request, 'about.html',)


def orders(request):
    '''
        There are three chances to enter this func:
            > /orders
            > /orders/place GET
            > /orders/place POST
    '''
    user = get_user(request)

    def clean_data(data) -> dict:
        '''
            > Checks:
                > check if any of the details exists excluding root_project if not and update order.
                > check if the project name already exists under the owner's order list
                > check if root_project is valid if order is for update
            > Returns:
                > return error in the data itself if any of the data is null
                > return error message if project name already exists
                > return data if all good
        '''
        nonlocal user

        is_update = data.get('is_update')
        if is_update:
            data['is_update'] = True
            usr_projs = Project.objects.all().filter(owner=user)
            root_proj = usr_projs.filter(project_name = data.get('root_project'))
            if not root_proj:
                data['msg'] = 'The root project doesn\'t exist'
                return data
            else:
                data['root_project'] = root_proj[0]
        else:
            data['is_update'] = False
            data.pop('root_project')
        if any(x == '' for x in data.values()):
            data['msg'] = 'Fill out the required fields'
        elif Project.objects.all().filter(owner= user).exists():
            rows = Project.objects.all().filter(owner= user)
            if any(row.project_name == data.get('project_name') for row in rows):
                data['msg'] = 'project name alredy used'
        return data


    if request.method == 'POST' and user.is_authenticated:
        data = clean_data({'project_name':request.POST.get('name'),'project_description':request.POST.get('description'),
                           'is_update':request.POST.get('is_update'),'root_project':request.POST.get('root_project')})

        if data.get('msg'):
            messages.warning(request, data.get('msg'))
            return redirect('/orders/place')
        print(data)
        table = Project(project_name = data.get('project_name'),project_description = data.get('project_description'),
                           is_update = data.get('is_update'),root_project = data.get('root_project'),  owner= user)
        table.save()
        messages.info(request, 'order placed successfully')
        return redirect('/orders/')
    else:
        data = {}
        if 'place' in request.path:
            if user.is_authenticated:
                data['show_form'] = True
            else:
                messages.warning(request, 'Plese sign in before ordering')
        data['orders'] = Project.objects.filter(owner=user)
        return render(request, 'orders.html', {'data':data})


def _404(request, exception):
    data = {'exp':exception}
    if not get_user(request).is_authenticated:
        data['msg'] = 'Page requested requires login'

    return render(request, '404.html',{'data':data})

@login_required
def project(request, **kwrgs):
    '''
        > it shows the perticular project details of the requested project if the project is of the logged-in user
        > the project details:
                > name
                > description
                > project status -> project finished date(if completed) -> project init date(if started)
                > project ordered date
                > owner -> link to user_account
                > team reviews
                > estimated_cost
    '''
    project_name = kwrgs['project_id']
    user = get_user(request)
    proj = Project.objects.filter(owner=user, project_name = project_name)
    if not proj.exists():
        messages.error(request, f'The requested project doesn\'t exist under the user "{user.username}"')
        return redirect('/orders')
    proj = proj[0]
    return render(request,'project.html', {'data':proj})

@login_required(redirect_field_name='/auth/login')
def user_profile(request, **kwrgs):
    '''
        > it shows the public user account of requested users if the user is logged in
        > user details:
            > username
            > email
            > full_name
            > is_employee
    '''
    target_user = kwrgs['target_usr']
    user = get_user(request)
    target_user = RalkzUser.objects.get(username=target_user)
    data = {
        'username':target_user.username,
        'email':target_user.email,
        'full_name': target_user.full_name,
        'is_employee': target_user.is_employee
    }
    return render(request, 'profile.html',{'data':data})