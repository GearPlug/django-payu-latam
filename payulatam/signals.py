import django.dispatch

valid_notification_received = django.dispatch.Signal()
invalid_notification_received = django.dispatch.Signal()

approved_transaction = django.dispatch.Signal()
declined_transaction = django.dispatch.Signal()
expired_transaction = django.dispatch.Signal()
