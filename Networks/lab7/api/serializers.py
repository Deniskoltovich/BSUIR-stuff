from rest_framework import serializers

from trade.models import Bill
from profiles.models import Customer
from products.models import Product, Category


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ['id', 'price', 'quantity', 'city', 'region', 'country', 'date', 'customer']

class CustomerlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
