from django import forms
from django.conf import settings

from payulatam.fields import PayuDateTimeField
from payulatam.models import PaymentNotification
from payulatam.utils import get_signature


class PaymentNotificationForm(forms.ModelForm):
    commision_pol_currency = forms.CharField(max_length=3, required=False)
    shipping_address = forms.CharField(max_length=50, required=False)
    shipping_city = forms.CharField(max_length=50, required=False)
    shipping_country = forms.CharField(max_length=2, required=False)
    office_phone = forms.CharField(max_length=20, required=False)
    nickname_seller = forms.CharField(max_length=150, required=False)
    nickname_buyer = forms.CharField(max_length=150, required=False)
    bank_referenced_name = forms.CharField(max_length=100, required=False)
    error_code_bank = forms.CharField(max_length=255, required=False)
    error_message_bank = forms.CharField(max_length=255, required=False)
    antifraud_merchant_id = forms.CharField(max_length=100, required=False)
    airline_code = forms.CharField(max_length=4, required=False)
    extra1 = forms.CharField(max_length=255, required=False)
    extra2 = forms.CharField(max_length=255, required=False)
    extra3 = forms.CharField(max_length=255, required=False)
    pse_bank = forms.CharField(max_length=255, required=False)
    pse_reference1 = forms.CharField(max_length=255, required=False)
    pse_reference2 = forms.CharField(max_length=255, required=False)
    pse_reference3 = forms.CharField(max_length=255, required=False)
    date = PayuDateTimeField()

    risk = forms.DecimalField(max_digits=64, decimal_places=2, required=False)
    commision_pol = forms.DecimalField(max_digits=64, decimal_places=2, required=False)
    transaction_bank_id = forms.CharField(max_length=255, required=False)
    cus = forms.CharField(max_length=64, required=False)
    authorization_code = forms.CharField(max_length=12, required=False)

    class Meta:
        model = PaymentNotification
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        sign = cleaned_data.get('sign')
        merchant_id = cleaned_data.get('merchant_id')
        reference_sale = cleaned_data.get('reference_sale')

        # Si el segundo decimal del parámetro value es cero, ejemplo: 150.00
        # El nuevo valor new_value para generar la firma debe ir con sólo un decimal así: 150.0.
        # Si el segundo decimal del parámetro value es diferente a cero, ejemplo: 150.26
        # El nuevo valor new_value para generar la firma debe ir con los dos decimales así: 150.26.
        value = cleaned_data.get('value')
        first_decimal = str(value).split('.')[-1][0]
        if first_decimal == '0':
            value = '{}.0'.format(str(value).split('.')[0])

        currency = cleaned_data.get('currency')
        state_pol = cleaned_data.get('state_pol')

        generated_sign = get_signature(settings.PAYU_API_KEY, merchant_id, reference_sale, value, currency, state_pol)

        if sign != generated_sign:
            raise forms.ValidationError('Invalid payment notification sign.')
