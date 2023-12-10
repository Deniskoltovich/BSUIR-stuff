from django.forms import ModelForm, Form
from requests.models import Request

class RequestCreationForm(ModelForm):

    class Meta:
        model = Request
        exclude = ('employee', 'status')

    def __init__(self, *args, **kwargs):
        super(RequestCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'