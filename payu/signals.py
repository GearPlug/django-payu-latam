import django.dispatch

valid_notification_received = django.dispatch.Signal()
invalid_notification_received = django.dispatch.Signal()
