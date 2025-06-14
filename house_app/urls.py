from django.urls import path

from . import views


urlpatterns = [
    path("house/create/", views.HouseCreateView.as_view(), name='create_house'),
    path("flat/create/", views.FlatCreateView.as_view(), name='create_flat'),
    path('house/<id>/', views.HouseFlatListView.as_view(), name='house-detail'),
    path("flat/update/<id>/", views.FlatUpdateStatusView.as_view()),
]
