from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def employee(request):
    print('*'*10,'info: Employee.views.employee() not designed','*'*10)
    return redirect('/career/')