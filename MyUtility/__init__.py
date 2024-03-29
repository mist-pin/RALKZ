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
