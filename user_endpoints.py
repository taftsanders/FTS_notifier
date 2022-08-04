import caller

def get_user_id(sso, token):
    return caller.user('/users/sso/' + sso, '?fields=id', token)

def get_reportees(sso, token):
    user_meta = caller.user('/users/sso/' + sso, '?fields=id', token)
    managerId = user_meta.get('id')
    return caller.user('/users', '?managerId=' + managerId, token)
