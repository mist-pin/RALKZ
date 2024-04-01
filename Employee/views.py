from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from Employee.models import Salary, Employee, Team
from Home.models import Project


@login_required
def employee(request):
    '''
        data{
            salary -> date, amount, project
            team_members -> date,emp_position,employee
            team_projects -> project,current_project
        }
    '''
    data = {}
    user = get_user(request)
    employee = Employee.objects.get(user_name = user)
    team = Team.objects.filter(employee = employee).order_by('-id')
    if team.exists():
        team = team[0]

    salary = Salary.objects.filter(employee = employee)
    data['salary'] = salary

    team_members = Team.objects.filter(team_name = team.team_name)
    data['team_members'] = team_members

    team_projects = Project.objects.filter(project_team = team.team_name).order_by('id')
    data['team_projects'] = team_projects

    return render(request, 'employee.html', {'data':data})