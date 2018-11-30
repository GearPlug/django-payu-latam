from django import forms

from payulatam.fields import PayuDateTimeField
from payulatam.models import PaymentNotification


class PaymentNotificationForm(forms.ModelForm):
    commision_pol_currency = forms.CharField(max_length=3, required=False)
    shipping_address = forms.CharField(widget=forms.Textarea, required=False)
    shipping_city = forms.CharField(max_length=255, required=False)
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

    billing_address = forms.CharField(widget=forms.Textarea, required=False)
    billing_city = forms.CharField(max_length=255, required=False)
    billing_country = forms.CharField(max_length=2, required=False)
    phone = forms.CharField(max_length=20, required=False)
    customer_number = forms.IntegerField(required=False)
    ip = forms.CharField(max_length=39, required=False)

    flag_code = forms.CharField(max_length=4, required=False)
    flag_info = forms.CharField(max_length=100, required=False)
    raw = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = PaymentNotification
        fields = '__all__'
