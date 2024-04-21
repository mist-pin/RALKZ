def check_data_to_update(base_data, **kwrgs):
    '''
        base_data: data from the database
        return only distinct non emty values to be updated in database
        check every kwrgs for empty and same in database
    '''


    values =  []
    for key, val in kwrgs.items():
        if key== 'password':
            # todo: use chek_password() and add to values list
            values.append({key:val})
            continue
        if eval(f'base_data.{key}') == val or  val.strip() == '':
            continue
        else:
            values.append({key:val})
    print('vals = ' , values)
    return values

def add_employee(user_name, emp_team, emp_position, emp_level=4):
    '''
        db_hierarchy:
            RalkzUser <- Aspirant

            RalkzUser <- Employee <- Salary
            RalkzUser <- Employee <- EmployeePosition
            RalkzUser <- Employee <- Team

            RalkzUser <- Project <- Score
            RalkzUser <- Project <- Salary
            RalkzUser <- Project <- Income

            ScoreAlloted <- Score
            ScoreAchived <- Score

        adding_employee:
            > add Employee - employee_id, user_name(user)
            > add Team - employee(Employee),team_name
            > add EmployeePosition - position, employee(Employee)
            > set RalkzUser.is_employee = True
            > set RalkzUser.is_aspirant = False
    '''


    from Employee.models import Employee, Team, EmployeePosition
    from Auth.models import RalkzUser

    try:
        user_obj = RalkzUser.objects.get(username=user_name)
    except RalkzUser.DoesNotExist:
        raise AttributeError("UserName is wrong")


    def _emp_id_generator() -> str:
        '''
            > structure: 'ralkz_+year+emp_count' ex: 'ralkz_+24+001' -> ralkz_240001
            > sort employees on the basis of join_date and select the last joined employee and get his emp_count for the next new employee
        '''
        import datetime
        year = str(datetime.datetime.now().year)[2:]
        prev_emp = Employee.objects.all().order_by('-employee_id')
        emp_count = '0001'
        if prev_emp.exists():
            prev_emp = prev_emp[0]
            emp_count = str(int(prev_emp.employee_id[-4:])+1)
            while len(emp_count) != 4:
                emp_count = f'0{emp_count}'

        emp_id = f'ralkz_{year}{emp_count}'
        return emp_id

    try:
        new_emp = Employee(employee_id=_emp_id_generator(), user_name= user_obj)
        position = EmployeePosition(position=emp_position, employee=new_emp, emp_level=emp_level)
        team = Team(team_name=emp_team, employee=new_emp)

        user_obj.is_employee = True
        user_obj.is_aspirant = False

        new_emp.save()
        position.save()
        team.save()
        user_obj.save()
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False




MD = 1
MAN = 2
EMP = 3

