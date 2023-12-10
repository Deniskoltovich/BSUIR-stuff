from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, BillViewSet, CategoryViewSet, CustomerViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(title='api-docs', default_version='v1'))

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'bill', BillViewSet)

router.register(r'customer', CustomerViewSet)




urlpatterns = [
    path('doc/', schema_view.with_ui()),
    path('', include(router.urls)),
]