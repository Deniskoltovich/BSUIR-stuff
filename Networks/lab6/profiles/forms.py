from django.forms import ModelForm

from profiles.models import Customer


class CustomerCreationForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
