from django.forms import ModelForm, Form

from users.models import Admin, Employee


from django import forms

from departments.models import Department

ACTIONS = (
    ('Delete', 'Удалить'),
    ('Add', 'Добавить')
)
class ChangeGroupForm(forms.Form):
    department_name = forms.CharField(label="Отдел группы", max_length=100)
    access_department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="отдел", label="Доступ к какому объекту Вы хотите поменять?")
    action = forms.ChoiceField(label="", choices=ACTIONS)

class ChangeUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label="сотрудник", label='Сотрудник')
    access_department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="отдел", label='Отдел')
    action = forms.ChoiceField(label="Действие", choices=ACTIONS)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='Новый пароль')



class AdminCreationForm(ModelForm):

    class Meta:
        model = Admin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdminCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EmployeeCreationForm(ModelForm):

    class Meta:
        model = Employee
        exclude = ('user_group',)

    def __init__(self, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'