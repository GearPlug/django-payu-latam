from django import forms
from django.utils.html import format_html

from payulatam.fields import PayuDateTimeField
from payulatam.models import PaymentNotification
from payulatam.settings import payulatam_settings


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

    test = forms.BooleanField(required=False)

    cc_number = forms.CharField(max_length=100, required=False)
    cc_holder = forms.CharField(max_length=100, required=False)
    franchise = forms.CharField(max_length=100, required=False)
    installments_number = forms.IntegerField(required=False)

    class Meta:
        model = PaymentNotification
        fields = '__all__'


class WebcheckoutPaymentForm(forms.Form):
    merchantId = forms.CharField(initial=payulatam_settings.MERCHANT_ID, max_length=100, widget=forms.HiddenInput)
    accountId = forms.CharField(initial=payulatam_settings.ACCOUNT_ID, max_length=100, widget=forms.HiddenInput)
    description = forms.CharField(max_length=100, widget=forms.HiddenInput)
    referenceCode = forms.CharField(max_length=100, widget=forms.HiddenInput)
    amount = forms.CharField(max_length=100, widget=forms.HiddenInput)
    tax = forms.CharField(max_length=100, widget=forms.HiddenInput)
    taxReturnBase = forms.CharField(max_length=100, widget=forms.HiddenInput)
    currency = forms.CharField(max_length=100, widget=forms.HiddenInput)
    signature = forms.CharField(max_length=100, widget=forms.HiddenInput)
    test = forms.CharField(initial=1, max_length=1, widget=forms.HiddenInput)
    buyerFullName = forms.CharField(max_length=200, widget=forms.HiddenInput)
    buyerEmail = forms.CharField(max_length=100, widget=forms.HiddenInput)
    telephone = forms.CharField(max_length=100, widget=forms.HiddenInput)
    responseUrl = forms.CharField(max_length=100, widget=forms.HiddenInput)
    confirmationUrl = forms.CharField(max_length=100, widget=forms.HiddenInput)

    def render(self):
        return format_html(u"""<form action="{0}" method="post">
            {1}
            <input type="image" src="{2}" border="0" name="submit" alt="Buy it Now" />
        </form>""", self.get_web_checkout_endpoint(), self.as_p(), self.get_image())

    def get_web_checkout_endpoint(self):
        return payulatam_settings.WEBCHECKOUT_URL

    def get_image(self):
        return payulatam_settings.PAYMENT_BUTTON_IMAGE_URL
