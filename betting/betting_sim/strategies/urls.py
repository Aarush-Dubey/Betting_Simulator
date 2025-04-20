from django.urls import path
from . import views

app_name = 'strategies'

urlpatterns = [
    path('', views.StrategyListView.as_view(), name='list'),
    path('create/', views.StrategyCreateView.as_view(), name='create'),
    path('<int:pk>/', views.StrategyDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.StrategyUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.StrategyDeleteView.as_view(), name='delete'),
    path('<int:pk>/download/', views.StrategyDownloadView.as_view(), name='download'),
    path('template/', views.StrategyTemplateView.as_view(), name='template'),
] 