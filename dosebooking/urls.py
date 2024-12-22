from django.urls import path
from .views import DoseBookingCreateView, CampaignReviewCreateView, DoseBookingListView, DoseBookingDetailView

urlpatterns = [
    path('create-review/', CampaignReviewCreateView.as_view(), name='create-review'),
    path('create-booking/', DoseBookingCreateView.as_view(), name='create-booking'),
    path('list-bookings/', DoseBookingListView.as_view(), name='list-bookings'),
    path('booking-detail/<int:pk>/', DoseBookingDetailView.as_view(), name='booking-detail'),
]
