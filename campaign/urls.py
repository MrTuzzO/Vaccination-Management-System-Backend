from django.urls import path, include
from .views import VaccineCampaignList, VaccineCampaignDetail

urlpatterns = [
    path('', VaccineCampaignList.as_view(), name='campaign-list'),
    path('<int:pk>/', VaccineCampaignDetail.as_view(), name='campaign-detail'),
]
