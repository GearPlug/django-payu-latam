try:
    # Try to import path from django 2.0+
    from django.urls import path
    url = 'notification/'
except:
    # If it breaks then we import url from django 1.X
    from django.conf.urls import url as path
    url = '^notification/$'

from payulatam.views import PaymentNotificationView

urlpatterns = [
    path(url, PaymentNotificationView.as_view(), name='notification'),
]
