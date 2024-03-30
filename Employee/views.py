from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def asdf(request):
    return render(request, 'employee.html')