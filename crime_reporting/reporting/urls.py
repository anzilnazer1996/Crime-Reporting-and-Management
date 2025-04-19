from django.urls import path

from . import views

urlpatterns = [
    
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),

    path('crime-list/',views.CrimeListView.as_view(),name='crime-list'),

    path('crime-details/<str:uuid>/',views.CrimeDetailsView.as_view(),name='crime-details'),

    path('crime-register/',views.CrimeRegisterView.as_view(),name='crime-register'),

]