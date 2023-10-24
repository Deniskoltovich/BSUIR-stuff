from django.forms import ModelForm

from products.models import Product, Category


class ProductCreationForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CategoryCreationForm(ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(CategoryCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'