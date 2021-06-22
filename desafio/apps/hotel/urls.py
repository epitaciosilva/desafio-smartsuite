from hotel import views

from rest_framework.routers import DefaultRouter

from django.urls import include, path

app_name = 'hotel'

router = DefaultRouter()
router.register('hotel', views.HotelViewSet)
router.register('tax', views.TaxViewSet)
router.register('reserve', views.ReserveViewSet)


v1_api_urlpatterns = [
    path('', include(router.urls)),
    path('cheapest/', views.Cheapest.as_view(), name='cheapest')
]

urlpatterns = [

]
