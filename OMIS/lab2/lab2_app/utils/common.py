from users.models import Employee, Admin

def get_current_user(request):
    r_user = request.user
    try:
        user = Employee.objects.get(fullname=r_user.username)
        return user, False
    except Exception:
        user = Admin.objects.get(fullname=r_user.username)
        return user, True