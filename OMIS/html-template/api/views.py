
from rest_framework import viewsets


from api.serializers import ProductSerializer, CategorySerializer, CustomerlSerializer, BillSerializer
from trade.models import Bill
from profiles.models import Customer
from products.models import Product, Category




class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all().order_by()
    serializer_class = BillSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by()
    serializer_class = CategorySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by()
    serializer_class = CustomerlSerializer

