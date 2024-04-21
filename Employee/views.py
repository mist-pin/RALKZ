from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from Employee.models import EmployeePosition, Salary, Employee, Team
from Home.models import Aspirants, Income, Project
from django.contrib import messages
from MyUtility import *


# employee
@login_required
def emp(request, employee):
    team = Team.objects.filter(employee = employee).order_by('-id')[0]
    salary = Salary.objects.filter(employee = employee)
    team_projects = Project.objects.filter(project_team = team.team_name).order_by('id')

    data = {
        'salary': salary,
        'team_projects':team_projects,
        'team_name': team.team_name,
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

    return render(request, 'employee_emp.html', {'data':data})


# team leader
@login_required
def tl(request, employee):
    '''
        > team lead
        > messaging: private msg with employees, team level messages, mailing options
    '''
    team = Team.objects.filter(employee = employee).order_by('-id')[0]
    salary = Salary.objects.filter(employee = employee)
    team_projects = Project.objects.filter(project_team = team.team_name).order_by('id')

    data = {
        'salary': salary,
        'team_projects':team_projects,
        'team_name': team.team_name,
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
    return render(request, 'employee_tl.html', {'data':data})


# project manager
@login_required
def pm(request):
    return render(request, 'employee_pm.html')


# head of project managers
@login_required
def hpm(request, **kwrgs):
    return render(request, 'employee_hpm.html')


# team manager
@login_required
def tm(request, **kwrgs):
    '''
        > his salary
        > team -> team name, employees link, employees points, team points
        > projects -> project name link, points per project, current project indication
        > job -> define one day work, allocate work for employees
        >
    '''
    return render(request, 'employee_tm.html')


# sales manager
@login_required
def sm(request, **kwrgs):
    '''
        > his salary
        > projects -> name, estimated cost and expences, advance payed, amount to be payd, actual income and expence, loss or gain
        > sales report per project
    '''
    return render(request, 'employee_sm.html')


# managing director
@login_required
def md(request):
    '''
        > managing director

        > duties :
            > select employees out of aspirants
            > review order from customer and assign to teams
            > define job posts available

        > data :
            > teams -> team name -> employee list
            > aspirants -> aspirant list
            > orders -> order list
            > finance -> transaction list

            > group points and their working criteria
            > particular employee points and their work analysis charts
            > particular and team mailing, messaging options
    '''
    user = get_user(request)
    employee = Employee.objects.get(user_name = user)

    team_data = Team.objects.all()
    teams = {}
    for team in team_data.values('team_name').distinct():
        team_emps = []
        for employee_obj in team_data.filter(team_name=team.get('team_name')):
            emp = {'employee_id': employee_obj.employee_id,
                   'employee_pos': EmployeePosition.objects.filter(employee=Employee.objects.get(employee_id = employee_obj.employee_id)).order_by('-date')[0].position,
                   }
            team_emps.append(emp)
        teams[team.get('team_name')] = team_emps

    data = {
        'salary':  Salary.objects.filter(employee = employee),
        'teams' : teams,
        'aspirants': Aspirants.objects.all().filter(user__is_employee = False),
        'orders':Project.objects.all().order_by('ordered_date'),
        'finance': Income.objects.all().order_by('time'),
    }
    return render(request, 'employee_md.html', {'data':data})


# employee account
@login_required
def employee_account(request, **kwrgs):
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
    return render(request, 'employee_account.html', {'data':data})



@login_required
def employee_home(request):
    '''
        > Only GetMethod will be handled here
        > according to the employee level requests are redirected
        > data{
            salary -> date, amount, project
            team_members -> date,emp_position,employee
            team_projects -> project,current_project
          }
    '''
    user = get_user(request)
    employee = Employee.objects.get(user_name = user)
    emp_pos_obj = EmployeePosition.objects.filter(employee = employee).order_by('-date')[0]
    emp_level = emp_pos_obj.emp_level
    emp_pos = emp_pos_obj.position
    if emp_level == EMP:
        if emp_pos == 'emp':
            return emp(request, employee)
        elif emp_pos == 'tl':
            return tl(request, employee)
    elif emp_level == MAN:
        '''
            pm: project manager,
            hpm: head of project manager
            tm: team manager
            sm: sales manager
        '''
        if emp_pos == 'pm':
            return redirect('pm/')
        elif emp_pos == 'tm':
            return redirect('tm/')
        elif emp_pos == 'hpm':
            return redirect('hpm/')
        elif emp_pos == 'sm':
            return redirect('sm/')
    elif emp_level == MD:
        return redirect('md/')
