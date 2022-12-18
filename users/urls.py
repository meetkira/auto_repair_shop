from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

urlpatterns = [
    path('signup/individual/', views.IndividualUserCreateView.as_view(), name='create individual user'),
    path('individual/list/', views.IndividualUserListView.as_view(), name='list individual user'),
    path('individual/', views.IndividualUserView.as_view(), name='get/update/delete individual user'),

    path('signup/entity/', views.EntityUserCreateView.as_view(), name='create entity user'),
    path('entity/list/', views.EntityUserListView.as_view(), name='list entity user'),
    path('entity/', views.EntityUserView.as_view(), name='get/update/delete entity user'),

    path("token/", TokenObtainPairView.as_view(), name='token'),
    path("token/refresh/", TokenRefreshView.as_view(), name='refresh_token'),
]
