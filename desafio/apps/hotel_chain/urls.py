from product import views

from rest_framework.routers import DefaultRouter

from django.urls import include, path

app_name = 'hotel_chain'

router = DefaultRouter()
router.register('hotel', views.HotelViewSet)
router.register('client_type', views.ClientType)
router.register('client', views.ClientViewSet)
router.register('hotel_client', views.HotelClientViewSet)
router.register('rate', views.RateViewSet)
router.register('reserve', views.ReserveViewSet)


v1_api_urlpatterns = [
    path('', include(router.urls))
]

urlpatterns = [

]
