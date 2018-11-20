from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from payu.enumerators import Country, Currency

from payulatam.settings import payulatam_settings as settings
from payulatam.signals import valid_notification_received, invalid_notification_received, approved_transaction, \
    declined_transaction, expired_transaction
from payulatam.utils import get_signature

COUNTRY = tuple(map(lambda x: (x.value, x.name), Country))
CURRENCY = tuple(map(lambda x: (x.value, x.name), Currency))


class AbstractAdministrativeSegment(models.Model):
    """

    """
    administrative_fee = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    administrative_fee_tax = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    administrative_fee_base = models.DecimalField(max_digits=64, decimal_places=2, default=0)

    class Meta:
        abstract = True


class AbstractBankSegment(models.Model):
    """

    """
    bank_id = models.CharField(max_length=255)
    bank_referenced_name = models.CharField(max_length=100)
    error_code_bank = models.CharField(max_length=255)
    error_message_bank = models.CharField(max_length=255)

    class Meta:
        abstract = True


class AbstractBillingSegment(models.Model):
    """

    """
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=255)
    billing_country = models.CharField(max_length=2, choices=COUNTRY)

    class Meta:
        abstract = True


class AbstractCreditCardSegment(models.Model):
    """

    """
    cc_number = models.CharField(max_length=100)
    cc_holder = models.CharField(max_length=100)
    franchise = models.CharField(max_length=100)
    installments_number = models.IntegerField()

    class Meta:
        abstract = True


class AbstractPolSegment(models.Model):
    response_code_pol = models.CharField(max_length=255)
    response_message_pol = models.CharField(max_length=255)
    state_pol = models.CharField(max_length=32)
    reference_pol = models.CharField(max_length=255)
    commision_pol = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    commision_pol_currency = models.CharField(max_length=3)

    class Meta:
        abstract = True

    @property
    def is_state_approved(self):
        return self.state_pol == '4'

    @property
    def is_state_declined(self):
        return self.state_pol == '6'

    @property
    def is_state_expired(self):
        return self.state_pol == '5'

    @property
    def is_approved(self):
        """
        Transaction approved

        Returns:

        """
        return self.response_message_pol == 'APPROVED'

    @property
    def is_payment_network_rejected(self):
        """
        Transaction rejected by financial institution

        Returns:

        """
        return self.response_message_pol == 'PAYMENT_NETWORK_REJECTED'

    @property
    def is_entity_declined(self):
        """
        Transaction rejected by the bank

        Returns:

        """
        return self.response_message_pol == 'ENTITY_DECLINED'

    @property
    def is_insufficient_funds(self):
        """
        Insufficient funds

        Returns:

        """
        return self.response_message_pol == 'INSUFFICIENT_FUNDS'

    @property
    def is_invalid_card(self):
        """
        Invalid card

        Returns:

        """
        return self.response_message_pol == 'INVALID_CARD'

    @property
    def is_contact_the_entity(self):
        """
        Contact the financial institution

        Returns:

        """
        return self.response_message_pol == 'CONTACT_THE_ENTITY'

    @property
    def is_bank_account_activation_error(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.response_message_pol == 'BANK_ACCOUNT_ACTIVATION_ERROR'

    @property
    def is_bank_account_not_authorized_for_automatic_debit(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.response_message_pol == 'BANK_ACCOUNT_NOT_AUTHORIZED_FOR_AUTOMATIC_DEBIT'

    @property
    def is_invalid_agency_bank_account(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.response_message_pol == 'INVALID_AGENCY_BANK_ACCOUNT'

    @property
    def is_invalid_bank_account(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.response_message_pol == 'INVALID_BANK_ACCOUNT'

    @property
    def is_invalid_invalid_bank(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.response_message_pol == 'INVALID_BANK'

    @property
    def is_expired_card(self):
        """
        Expired card

        Returns:

        """
        return self.response_message_pol == 'EXPIRED_CARD'

    @property
    def is_restricted_card(self):
        """
        Restricted card

        Returns:

        """
        return self.response_message_pol == 'RESTRICTED_CARD'

    @property
    def is_invalid_expiration_date_or_security_code(self):
        """
        Invalid expiration date or security code

        Returns:

        """
        return self.response_message_pol == 'INVALID_EXPIRATION_DATE_OR_SECURITY_CODE'

    @property
    def is_repeat_transaction(self):
        """
        Retry payment

        Returns:

        """
        return self.response_message_pol == 'REPEAT_TRANSACTION'

    @property
    def is_invalid_transaction(self):
        """
        Invalid transaction

        Returns:

        """
        return self.response_message_pol == 'INVALID_TRANSACTION'

    @property
    def is_exceeded_amount(self):
        """
        The value exceeds the maximum allowed by the entity

        Returns:

        """
        return self.response_message_pol == 'EXCEEDED_AMOUNT'

    @property
    def is_abandoned_transaction(self):
        """
        Transaction abandoned by the payer

        Returns:

        """
        return self.response_message_pol == 'ABANDONED_TRANSACTION'

    @property
    def is_credit_card_not_authorized_for_internet_transaction(self):
        """
        Card not authorized to buy online

        Returns:

        """
        return self.response_message_pol == 'CREDIT_CARD_NOT_AUTHORIZED_FOR_INTERNET_TRANSACTIONS'

    @property
    def is_antifraud_rejected(self):
        """
        Transaction refused because of suspected fraud

        Returns:

        """
        return self.response_message_pol == 'ANTIFRAUD_REJECTED'

    @property
    def is_expired_transaction(self):
        """
        Expired transaction

        Returns:

        """
        return self.response_message_pol == 'EXPIRED_TRANSACTION'

    def get_state(self):
        # TODO devolver enum
        return self.state_pol

    def get_response_message(self):
        # TODO devolver enum
        return self.response_message_pol


class AbstractPSESegment(models.Model):
    pse_bank = models.CharField(max_length=255)
    pse_reference1 = models.CharField(max_length=255)
    pse_reference3 = models.CharField(max_length=255)
    pse_reference2 = models.CharField(max_length=255)

    class Meta:
        abstract = True


class AbstractShippingSegment(models.Model):
    """

    """
    shipping_address = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=2, choices=COUNTRY)

    class Meta:
        abstract = True


class AbstractTransactionSegment(models.Model):
    """

    """
    transaction_id = models.CharField(max_length=36, db_index=True)
    transaction_date = models.DateTimeField()
    transaction_bank_id = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.transaction_id


class AbstractValueSegment(models.Model):
    """

    """
    value = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    additional_value = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    exchange_rate = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY)

    class Meta:
        abstract = True


class AbstractFlagSegment(models.Model):
    flag = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def is_flagged(self):
        return self.flag

    def save(self, *args, **kwargs):
        exists = PaymentNotification.objects.filter(transaction_id=self.transaction_id).exists()
        if not self.id and exists:
            self.flag = True
        super().save(*args, **kwargs)


class AbstractPaymentNotification(AbstractAdministrativeSegment,
                                  AbstractBankSegment,
                                  AbstractBillingSegment,
                                  AbstractCreditCardSegment,
                                  AbstractPolSegment,
                                  AbstractPSESegment,
                                  AbstractShippingSegment,
                                  AbstractTransactionSegment,
                                  AbstractValueSegment,
                                  AbstractFlagSegment,
                                  ):
    """

    """
    payment_method = models.IntegerField()
    payment_method_id = models.IntegerField()
    payment_method_type = models.IntegerField()
    payment_method_name = models.CharField(max_length=255)
    payment_request_state = models.CharField(max_length=32)

    description = models.TextField()

    class Meta:
        abstract = True


class PaymentNotification(AbstractPaymentNotification):
    reference_sale = models.CharField(max_length=255)

    risk = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    sign = models.CharField(max_length=255)

    email_buyer = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    office_phone = models.CharField(max_length=20)

    merchant_id = models.IntegerField()

    customer_number = models.IntegerField()

    nickname_seller = models.CharField(max_length=150)
    nickname_buyer = models.CharField(max_length=150)

    antifraud_merchant_id = models.CharField(max_length=100)
    airline_code = models.CharField(max_length=4)
    cus = models.CharField(max_length=64)
    authorization_code = models.CharField(max_length=12)

    extra1 = models.CharField(max_length=255)
    extra2 = models.CharField(max_length=255)
    extra3 = models.CharField(max_length=255)

    attempts = models.IntegerField()
    ip = models.CharField(max_length=39)

    date = models.DateTimeField()
    test = models.BooleanField()

    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payu_payment_notification'

    def save(self, *args, **kwargs):
        if not self.id:
            # Si el segundo decimal del parámetro value es cero, ejemplo: 150.00
            # El nuevo valor new_value para generar la firma debe ir con sólo un decimal así: 150.0.
            # Si el segundo decimal del parámetro value es diferente a cero, ejemplo: 150.26
            # El nuevo valor new_value para generar la firma debe ir con los dos decimales así: 150.26.
            value = None
            first_decimal = str(self.value).split('.')[-1][0]
            if first_decimal == '0':
                value = '{}.0'.format(str(self.value).split('.')[0])

            sign = get_signature(settings.API_KEY, self.merchant_id, self.reference_sale, value, self.currency,
                                 self.state_pol)

            if self.sign != sign:
                self.flag = True
        super().save(*args, **kwargs)


@receiver(post_save, sender=PaymentNotification)
def payment_notification_save(sender, instance, created, **kwargs):
    if created:
        if instance.is_flagged:
            invalid_notification_received.send(sender=PaymentNotification)
        else:
            valid_notification_received.send(sender=PaymentNotification)

        if instance.is_state_approved:
            approved_transaction.send(sender=PaymentNotification)
        elif instance.is_state_declined:
            declined_transaction.send(sender=PaymentNotification)
        elif instance.is_state_expired:
            expired_transaction.send(sender=PaymentNotification)
        else:
            # TODO raise error
            pass
