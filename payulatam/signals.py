import django.dispatch

valid_notification_received = django.dispatch.Signal(providing_args=['instance'])
invalid_notification_received = django.dispatch.Signal(providing_args=['instance'])

payment_was_approved = django.dispatch.Signal(providing_args=['instance'])
payment_was_declined = django.dispatch.Signal(providing_args=['instance'])
payment_was_expired = django.dispatch.Signal(providing_args=['instance'])
payment_was_flagged = django.dispatch.Signal(providing_args=['instance'])
