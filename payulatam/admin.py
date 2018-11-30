from django.contrib import admin
from payu.enumerators import StatePol

from payulatam.models import PaymentNotification


class StatePolListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'state pol'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'state_pol'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return tuple(map(lambda x: (x.value, x.name), StatePol))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(state_pol=self.value())


class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id', 'reference_sale', 'state_pol_name', 'response_message_pol', 'test', 'flag', 'date_created'
    )
    list_filter = (StatePolListFilter, 'response_message_pol', 'test', 'flag')
    search_fields = ['transaction_id', 'reference_sale']
    fieldsets = (
        (None, {
            'fields': (
                'transaction_id', 'reference_sale', 'description', 'transaction_date', 'transaction_bank_id', 'value',
                'additional_value', 'tax', 'exchange_rate', 'currency')
        }),
        ('Payment', {
            'classes': ('collapse',),
            'fields': (
                'payment_method', 'payment_method_id', 'payment_method_type', 'payment_method_name',
                'payment_request_state', 'risk', 'sign', 'airline_code', 'authorization_code', 'extra1', 'extra2',
                'extra3', 'attempts', 'ip', 'date'),
        }),
        ('Administrative', {
            'classes': ('collapse',),
            'fields': ('administrative_fee', 'administrative_fee_tax', 'administrative_fee_base'),
        }),
        ('Bank', {
            'classes': ('collapse',),
            'fields': ('bank_id', 'bank_referenced_name', 'error_code_bank', 'error_message_bank'),
        }),
        ('Billing', {
            'classes': ('collapse',),
            'fields': ('billing_address', 'billing_city', 'billing_country'),
        }),
        ('Buyer', {
            'classes': ('collapse',),
            'fields': ('email_buyer', 'nickname_buyer', 'phone', 'office_phone'),
        }),
        ('Credit Card', {
            'classes': ('collapse',),
            'fields': ('cc_number', 'cc_holder', 'franchise', 'installments_number'),
        }),
        ('Merchant', {
            'classes': ('collapse',),
            'fields': ('merchant_id', 'nickname_seller', 'customer_number', 'antifraud_merchant_id'),
        }),
        ('POL', {
            'classes': ('collapse',),
            'fields': ('response_code_pol', 'response_message_pol', 'state_pol', 'reference_pol', 'commision_pol',
                       'commision_pol_currency'),
        }),
        ('PSE', {
            'classes': ('collapse',),
            'fields': ('cus', 'pse_bank', 'pse_reference1', 'pse_reference3', 'pse_reference2'),
        }),
        ('Shipping', {
            'classes': ('collapse',),
            'fields': ('shipping_address', 'shipping_city', 'shipping_country'),
        }),
        ('Admin', {
            'classes': ('collapse',),
            'fields': ('flag', 'flag_code', 'flag_info', 'test', 'raw'),
        }),
    )

    def state_pol_name(self, obj):
        return obj.get_state_name()

    state_pol_name.short_description = 'State Pol'


admin.site.register(PaymentNotification, PaymentNotificationAdmin)
