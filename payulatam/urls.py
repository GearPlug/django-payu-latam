from django.urls import path

from payulatam.views import PaymentNotificationView

urlpatterns = [
    path('notification/', PaymentNotificationView.as_view(), name='notification'),
]
