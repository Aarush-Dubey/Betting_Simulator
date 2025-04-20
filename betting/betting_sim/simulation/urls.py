from django.urls import path
from . import views

app_name = 'simulation'

urlpatterns = [
    path('', views.SimulationListView.as_view(), name='list'),
    path('create/', views.SimulationCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SimulationDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.SimulationUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.SimulationDeleteView.as_view(), name='delete'),
    path('<int:pk>/run/', views.RunSimulationView.as_view(), name='run'),
    path('result/<int:pk>/', views.SimulationResultView.as_view(), name='result'),
    path('result/<int:pk>/export/', views.ExportResultView.as_view(), name='export_result'),
] 