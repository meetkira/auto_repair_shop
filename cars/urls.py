from django.urls import path

from cars import views

urlpatterns = [
    path('create/', views.CarCreateView.as_view(), name='create car'),
    path('', views.CarListView.as_view(), name='list cars'),
    path('user/', views.UsersCarListView.as_view(), name='list users cars'),
    path('car/<int:pk>/', views.CarView.as_view(), name='get/update/delete car'),
]
