
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, mixins

from api.serializers import ProductSerializer, CategorySerializer, CustomerlSerializer, BillSerializer
from trade.models import Bill
from profiles.models import Customer
from products.models import Product, Category

class BillViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Bill.objects.all().order_by()
    serializer_class = BillSerializer

    @swagger_auto_schema(operation_description="Получить список накладных.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить накладную ID.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать накладную.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить информацию о накладной.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class ProductViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Product.objects.all().order_by()
    serializer_class = ProductSerializer

    @swagger_auto_schema(operation_description="Получить список товаров.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить товар по ID.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать товар.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить информацию о товаре.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,  mixins.DestroyModelMixin):
    queryset = Category.objects.all().order_by()
    serializer_class = CategorySerializer

    @swagger_auto_schema(operation_description="Получить список категорий.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить категорию по ID.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать категорию.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить информацию о категории.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
class CustomerViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,  mixins.DestroyModelMixin):
    queryset = Customer.objects.all().order_by()
    serializer_class = CustomerlSerializer

    @swagger_auto_schema(operation_description="Получить список покупателей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить покупателя по id")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать покупателя")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an existing customer.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

