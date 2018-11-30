from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from payu.enumerators import Currency, MessagePol, StatePol

from payulatam.settings import payulatam_settings as settings
from payulatam.signals import invalid_notification_received, payment_was_approved, payment_was_declined, \
    payment_was_expired, payment_was_flagged, valid_notification_received
from payulatam.utils import get_signature

CURRENCY = tuple(map(lambda x: (x.value, x.value), Currency))


class AbstractAdministrativeSegment(models.Model):
    administrative_fee = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    administrative_fee_tax = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    administrative_fee_base = models.DecimalField(max_digits=64, decimal_places=2, default=0)

    class Meta:
        abstract = True


class AbstractBankSegment(models.Model):
    bank_id = models.CharField(max_length=255)
    bank_referenced_name = models.CharField(max_length=100)
    error_code_bank = models.CharField(max_length=255)
    error_message_bank = models.CharField(max_length=255)

    class Meta:
        abstract = True


class AbstractBillingSegment(models.Model):
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=255)
    billing_country = models.CharField(max_length=2)

    class Meta:
        abstract = True


class AbstractCreditCardSegment(models.Model):
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
        return self.get_state() == StatePol.APPROVED

    @property
    def is_state_declined(self):
        return self.get_state() == StatePol.DECLINED

    @property
    def is_state_expired(self):
        return self.get_state() == StatePol.EXPIRED

    @property
    def is_approved(self):
        """
        Transaction approved

        Returns:

        """
        return self.get_response_message() == MessagePol.APPROVED

    @property
    def is_payment_network_rejected(self):
        """
        Transaction rejected by financial institution

        Returns:

        """
        return self.get_response_message() == MessagePol.PAYMENT_NETWORK_REJECTED

    @property
    def is_entity_declined(self):
        """
        Transaction rejected by the bank

        Returns:

        """
        return self.get_response_message() == MessagePol.ENTITY_DECLINED

    @property
    def is_insufficient_funds(self):
        """
        Insufficient funds

        Returns:

        """
        return self.get_response_message() == MessagePol.INSUFFICIENT_FUNDS

    @property
    def is_invalid_card(self):
        """
        Invalid card

        Returns:

        """
        return self.get_response_message() == MessagePol.INVALID_CARD

    @property
    def is_contact_the_entity(self):
        """
        Contact the financial institution

        Returns:

        """
        return self.get_response_message() == MessagePol.CONTACT_THE_ENTITY

    @property
    def is_bank_account_activation_error(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.get_response_message() == MessagePol.BANK_ACCOUNT_ACTIVATION_ERROR

    @property
    def is_bank_account_not_authorized_for_automatic_debit(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.get_response_message() == MessagePol.BANK_ACCOUNT_NOT_AUTHORIZED_FOR_AUTOMATIC_DEBIT

    @property
    def is_invalid_agency_bank_account(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.get_response_message() == MessagePol.INVALID_AGENCY_BANK_ACCOUNT

    @property
    def is_invalid_bank_account(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.get_response_message() == MessagePol.INVALID_BANK_ACCOUNT

    @property
    def is_invalid_invalid_bank(self):
        """
        Automatic debit is not allowed

        Returns:

        """
        return self.get_response_message() == MessagePol.INVALID_BANK

    @property
    def is_expired_card(self):
        """
        Expired card

        Returns:

        """
        return self.get_response_message() == MessagePol.EXPIRED_CARD

    @property
    def is_restricted_card(self):
        """
        Restricted card

        Returns:

        """
        return self.get_response_message() == MessagePol.RESTRICTED_CARD

    @property
    def is_invalid_expiration_date_or_security_code(self):
        """
        Invalid expiration date or security code

        Returns:

        """
        return self.get_response_message() == MessagePol.INVALID_EXPIRATION_DATE_OR_SECURITY_CODE

    @property
    def is_repeat_transaction(self):
        """
        Retry payment

        Returns:

        """
        return self.get_response_message() == MessagePol.REPEAT_TRANSACTION

    @property
    def is_invalid_transaction(self):
        """
        Invalid transaction

        Returns:

        """
        return self.get_response_message() == MessagePol.INVALID_TRANSACTION

    @property
    def is_exceeded_amount(self):
        """
        The value exceeds the maximum allowed by the entity

        Returns:

        """
        return self.get_response_message() == MessagePol.EXCEEDED_AMOUNT

    @property
    def is_abandoned_transaction(self):
        """
        Transaction abandoned by the payer

        Returns:

        """
        return self.get_response_message() == MessagePol.ABANDONED_TRANSACTION

    @property
    def is_credit_card_not_authorized_for_internet_transaction(self):
        """
        Card not authorized to buy online

        Returns:

        """
        return self.get_response_message() == MessagePol.CREDIT_CARD_NOT_AUTHORIZED_FOR_INTERNET_TRANSACTIONS

    @property
    def is_antifraud_rejected(self):
        """
        Transaction refused because of suspected fraud

        Returns:

        """
        return self.get_response_message() == MessagePol.ANTIFRAUD_REJECTED

    @property
    def is_digital_certificate_not_found(self):
        """
        Digital certificate not found

        Returns:

        """
        return self.get_response_message() == MessagePol.DIGITAL_CERTIFICATE_NOT_FOUND

    @property
    def is_bank_unreachable(self):
        """
        Error trying to communicate with the bank

        Returns:

        """
        return self.get_response_message() == MessagePol.BANK_UNREACHABLE

    @property
    def is_payment_network_no_connection(self):
        """
        Unable to communicate with the financial institution

        Returns:

        """
        return self.get_response_message() == MessagePol.PAYMENT_NETWORK_NO_CONNECTION

    @property
    def is_payment_network_no_response(self):
        """
        No response was received from the financial institution

        Returns:

        """
        return self.get_response_message() == MessagePol.PAYMENT_NETWORK_NO_RESPONSE

    @property
    def is_entity_messaging_error(self):
        """
        Error communicating with the financial institution

        Returns:

        """
        return self.get_response_message() == MessagePol.ENTITY_MESSAGING_ERROR

    @property
    def is_not_accepted_transaction(self):
        """
        Transaction not permitted

        Returns:

        """
        return self.get_response_message() == MessagePol.NOT_ACCEPTED_TRANSACTION

    @property
    def is_internal_payment_provider_error(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.INTERNAL_PAYMENT_PROVIDER_ERROR

    @property
    def is_inactive_payment_provider(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.INACTIVE_PAYMENT_PROVIDER

    @property
    def is_error(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.ERROR

    @property
    def is_error_converting_transactions_amounts(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.ERROR_CONVERTING_TRANSACTION_AMOUNTS

    @property
    def is_fix_not_required(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.FIX_NOT_REQUIRED

    @property
    def is_automatically_fixed_and_success_reversal(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.AUTOMATICALLY_FIXED_AND_SUCCESS_REVERSAL

    @property
    def is_automatically_fixed_and_unsuccess_reversal(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.AUTOMATICALLY_FIXED_AND_UNSUCCESS_REVERSAL

    @property
    def is_automatic_fixed_not_supported(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.AUTOMATIC_FIXED_NOT_SUPPORTED

    @property
    def is_not_fixed_for_error_state(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.NOT_FIXED_FOR_ERROR_STATE

    @property
    def is_error_fixing_and_reversing(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.ERROR_FIXING_AND_REVERSING

    @property
    def is_error_fixing_incomplete_data(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.ERROR_FIXING_INCOMPLETE_DATA

    @property
    def is_payment_network_bad_response(self):
        """
        Error

        Returns:

        """
        return self.get_response_message() == MessagePol.PAYMENT_NETWORK_BAD_RESPONSE

    @property
    def is_expired_transaction(self):
        """
        Expired transaction

        Returns:

        """
        return self.get_response_message() == MessagePol.EXPIRED_TRANSACTION

    def get_state(self):
        try:
            return StatePol(self.state_pol)
        except ValueError:
            return self.state_pol

    def get_state_name(self):
        state = self.get_state()
        return state.name if isinstance(state, StatePol) else state

    def get_response_message(self):
        try:
            return MessagePol(self.response_message_pol)
        except ValueError:
            return self.response_message_pol


class AbstractPSESegment(models.Model):
    cus = models.CharField(max_length=64)
    pse_bank = models.CharField(max_length=255)
    pse_reference1 = models.CharField(max_length=255)
    pse_reference3 = models.CharField(max_length=255)
    pse_reference2 = models.CharField(max_length=255)

    class Meta:
        abstract = True


class AbstractShippingSegment(models.Model):
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=2)

    class Meta:
        abstract = True


class AbstractTransactionSegment(models.Model):
    transaction_id = models.CharField(max_length=36, db_index=True)
    transaction_date = models.DateTimeField()
    transaction_bank_id = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.transaction_id


class AbstractValueSegment(models.Model):
    value = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    additional_value = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    exchange_rate = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY)

    class Meta:
        abstract = True


class AbstractFlagSegment(models.Model):
    DUPLICATE_TRANSACTION = '1001'
    INVALID_SIGN = '1002'
    FLAG_CODES = (
        (DUPLICATE_TRANSACTION, 'Duplicate Transaction'),
        (INVALID_SIGN, 'Invalid Sign'),
    )
    flag = models.BooleanField(default=False)
    flag_code = models.CharField(max_length=4, choices=FLAG_CODES)
    flag_info = models.CharField(max_length=100)

    class Meta:
        abstract = True

    @property
    def is_flagged(self):
        return self.flag

    def save(self, *args, **kwargs):
        exists = PaymentNotification.objects.filter(transaction_id=self.transaction_id).exists()
        if not self.id and exists:
            self.flag = True
            self.flag_code = self.DUPLICATE_TRANSACTION
            self.flag_info = 'Duplicate transaction_id. ({})'.format(self.transaction_id)
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
    payment_method = models.IntegerField()
    payment_method_id = models.IntegerField()
    payment_method_type = models.IntegerField()
    payment_method_name = models.CharField(max_length=255)
    payment_request_state = models.CharField(max_length=32)

    class Meta:
        abstract = True


class PaymentNotification(AbstractPaymentNotification):
    reference_sale = models.CharField(max_length=255)
    description = models.TextField()

    risk = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True)
    sign = models.CharField(max_length=255)

    email_buyer = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    office_phone = models.CharField(max_length=20)

    merchant_id = models.IntegerField()

    customer_number = models.IntegerField(blank=True, null=True)

    nickname_seller = models.CharField(max_length=150)
    nickname_buyer = models.CharField(max_length=150)

    antifraud_merchant_id = models.CharField(max_length=100)
    airline_code = models.CharField(max_length=4)
    authorization_code = models.CharField(max_length=12)

    extra1 = models.CharField(max_length=255)
    extra2 = models.CharField(max_length=255)
    extra3 = models.CharField(max_length=255)

    attempts = models.IntegerField()
    ip = models.CharField(max_length=39)

    date = models.DateTimeField()
    test = models.BooleanField()

    raw = models.TextField()

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
                self.flag_code = AbstractFlagSegment.INVALID_SIGN
                self.flag_info = 'Invalid sign. ({})'.format(self.sign)
        super().save(*args, **kwargs)


@receiver(post_save, sender=PaymentNotification)
def payment_notification_save(sender, instance, created, **kwargs):
    if created:
        if instance.is_flagged:
            invalid_notification_received.send(sender=PaymentNotification, instance=instance)
            payment_was_flagged.send(sender=PaymentNotification, instance=instance)
            return
        else:
            valid_notification_received.send(sender=PaymentNotification, instance=instance)

        if instance.is_state_approved:
            payment_was_approved.send(sender=PaymentNotification, instance=instance)
        elif instance.is_state_declined:
            payment_was_declined.send(sender=PaymentNotification, instance=instance)
        elif instance.is_state_expired:
            payment_was_expired.send(sender=PaymentNotification, instance=instance)
        else:
            # TODO raise error
            pass
