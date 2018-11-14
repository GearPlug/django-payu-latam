from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from payulatam.signals import valid_notification_received, invalid_notification_received



class AbstractTransactionNotification(models.Model):
    """

    """
    transaction_id = models.CharField(max_length=36, db_index=True)
    transaction_date = models.DateTimeField()

    # TODO: Revisar si es de bank o transaction
    transaction_bank_id = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.transaction_id


class AbstractBillingNotification(models.Model):
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=255)
    billing_country = models.CharField(max_length=2)  # TODO: choices

    class Meta:
        abstract = True


class AbstractShippingNotification(models.Model):
    shipping_address = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=2)  # TODO: choices

    class Meta:
        abstract = True


class PaymentNotification(models.Model):
    reference_sale = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    payment_method = models.IntegerField()
    payment_method_id = models.IntegerField()
    payment_method_type = models.IntegerField()
    payment_method_name = models.CharField(max_length=255)
    payment_request_state = models.CharField(max_length=32)
    cc_number = models.CharField(max_length=100)
    cc_holder = models.CharField(max_length=100)
    franchise = models.CharField(max_length=100)
    installments_number = models.IntegerField()

    value = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    additional_value = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    administrative_fee = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    administrative_fee_tax = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    administrative_fee_base = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    exchange_rate = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    currency = models.CharField(max_length=3)
    risk = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    sign = models.CharField(max_length=255)

    response_code_pol = models.CharField(max_length=255)
    response_message_pol = models.CharField(max_length=255)
    state_pol = models.CharField(max_length=32)
    reference_pol = models.CharField(max_length=255)
    commision_pol = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    commision_pol_currency = models.CharField(max_length=3)

    email_buyer = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    office_phone = models.CharField(max_length=20)

    merchant_id = models.IntegerField()
    customer_number = models.IntegerField()

    nickname_seller = models.CharField(max_length=150)
    nickname_buyer = models.CharField(max_length=150)

    bank_id = models.CharField(max_length=255)
    bank_referenced_name = models.CharField(max_length=100)
    # transaction_bank_id = models.CharField(max_length=255)
    error_code_bank = models.CharField(max_length=255)
    error_message_bank = models.CharField(max_length=255)

    antifraud_merchant_id = models.CharField(max_length=100)
    airline_code = models.CharField(max_length=4)
    cus = models.CharField(max_length=64)
    authorization_code = models.CharField(max_length=12)

    extra1 = models.CharField(max_length=255)
    extra2 = models.CharField(max_length=255)
    extra3 = models.CharField(max_length=255)

    pse_bank = models.CharField(max_length=255)
    pse_reference1 = models.CharField(max_length=255)
    pse_reference3 = models.CharField(max_length=255)
    pse_reference2 = models.CharField(max_length=255)

    attempts = models.IntegerField()
    ip = models.CharField(max_length=39)

    date = models.DateTimeField()
    test = models.BooleanField()

    flag = models.BooleanField()

    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payu_payment_notification'

    def save(self, *args, **kwargs):
        if not self.id:
            exists = PaymentNotification.objects.filter(transaction_id=self.transaction_id).exists()
            if exists:
                self.flag = True
        super().save(*args, **kwargs)

    @property
    def is_flagged(self):
        return self.flag


@receiver(post_save, sender=PaymentNotification)
def payment_notification_save(sender, instance, created, **kwargs):
    if created:
        if instance.is_flagged:
            invalid_notification_received.send(sender=PaymentNotification)
        else:
            valid_notification_received.send(sender=PaymentNotification)
