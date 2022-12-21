from django.urls import path

from orders import views

urlpatterns = [
    path('spare_parts/create/', views.SparePartCreateView.as_view(), name='create spare part'),
    path('spare_parts/spare_part/<int:pk>/', views.SparePartView.as_view(), name='get spare part'),
    path('spare_parts/', views.SparePartListView.as_view(), name='list spare parts'),

    path('purchases/create/', views.PurchaseCreateView.as_view(), name='create purchase'),
    path('purchases/purchase/<int:pk>/', views.PurchaseView.as_view(), name='get purchase'),
    path('purchases/', views.PurchaseListView.as_view(), name='list purchases'),
]
