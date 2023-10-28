from django.forms import ModelForm

from trade.models import Bill


class BillCreationForm(ModelForm):

    class Meta:
        model = Bill
        exclude = ['full_price',]


    def __init__(self, *args, **kwargs):
        super(BillCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

