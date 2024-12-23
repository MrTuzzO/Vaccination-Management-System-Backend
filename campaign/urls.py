from django.urls import path, include
from .views import VaccineCampaignList, VaccineCampaignDetail
from dosebooking.views import ReviewListView

urlpatterns = [
    path('', VaccineCampaignList.as_view(), name='campaign-list'),
    path('<int:pk>/', VaccineCampaignDetail.as_view(), name='campaign-detail'),
    path('<int:pk>/reviews/', ReviewListView.as_view(), name='campaign-detail'),
]
