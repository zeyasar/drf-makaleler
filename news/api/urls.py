from django.urls import path
from news.api import views as api_views



urlpatterns = [
    path('yazarlar/',api_views.GazeteciListCreateApiView.as_view(), name='yazar-listesi'),
    path('makaleler', api_views.MakaleListCreateApiView.as_view(), name='makale-listesi'),
    path('makaleler/<int:pk>/', api_views.MakaleDetailApiView.as_view(), name='makale-detay'),
]