from django.urls import path

from payu.views import PaymentNotificationView

urlpatterns = [
    path('notification/', PaymentNotificationView.as_view(), name='notification'),
]
