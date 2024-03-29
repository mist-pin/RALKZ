from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from Auth.models import RalkzUser
from Home.models import Aspirants

def home(request):
    return render(request, 'home.html')


def faq(request):
    return render(request, 'faq.html')


def career(request):
    data = {}
    if Aspirants.objects.exists():
        user = get_user(request)
        if db:= Aspirants.objects.filter(user=user):
            data['application_status'] = db[0].application_status
    return render(request, 'career.html', {'data':data})

@login_required
def apply_job(request):
    user = get_user(request)
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
