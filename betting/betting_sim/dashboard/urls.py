from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),
    path('compare/<int:pk1>/<int:pk2>/', views.CompareResultsView.as_view(), name='compare'),
] 