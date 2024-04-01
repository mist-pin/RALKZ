from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from Employee.models import EmployeePosition, Salary, Employee, Team
from Home.models import Project
from django.contrib import messages

@login_required
def employee_home(request):
    '''
        Only GetMethod will be handled here
        data{
            salary -> date, amount, project
            team_members -> date,emp_position,employee
            team_projects -> project,current_project
        }
    '''
    user = get_user(request)
    employee = Employee.objects.get(user_name = user)
    team = Team.objects.filter(employee = employee).order_by('-id')[0]
    salary = Salary.objects.filter(employee = employee)
    team_projects = Project.objects.filter(project_team = team.team_name).order_by('id')
    data = {
        'salary': salary,
        'team_projects':team_projects,
        'team_members': [
            {
                'date': member.date,
                'employee': member.employee,
                'emp_position': EmployeePosition.objects.filter(
                    employee=member.employee
                )
                .order_by('-date')[0]
                .position,
            }
            for member in Team.objects.filter(team_name=team.team_name, employee__user_name__is_employee=True)
        ]
    }

    return render(request, 'employee_home.html', {'data':data})


@login_required
def employee(request, **kwrgs):
    '''
        > it is an employee account home page
        > any logged in user can access this
        > check if the current user is the employee and give edit options
        > details:
            > employee_id
            > username link
            > team
            > scores
    '''
    user = get_user(request)
    employee = Employee.objects.filter(employee_id = kwrgs['emp_id'])
    if not employee.exists():
        messages.error(request, f"The requested employee, {kwrgs['emp_id']} doesn't exist")
        return redirect('/emp')
    employee = employee[0]
    data = {
        'employee_id': employee.employee_id,
        'user_name': employee.user_name,
        'team': Team.objects.filter(employee=employee).order_by('-date')[0].team_name,
        'score':None
    }
    return render(request, 'employee.html', {'data':data})



