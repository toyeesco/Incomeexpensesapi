from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncomeListAPIView.as_view(), name='expenses'),
    path('<int:id>', views.IncomeDetailAPIView.as_view(), name='expenses-detail')
]