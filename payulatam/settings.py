"""
    This module follows the approach of the JazzBand django apps.

    The 'settings.py' file might look like this:

    PAYU_LATAM = {
        'API_LOGIN': 'pRRXKOl8ikMmt9u', # This is the Payu test API LOGIN
        'API_KEY':  '4Vj8eK4rloUd272L48hsrarnUA', # This is the Payu test API KEY
        'MERCHANT_ID': 12345, # Please change this
        'ACCOUNT_ID_DICT': {
            'CO': 54321 # Also change this.
        }
    }
"""
from django.conf import settings

USER_SETTINGS = getattr(settings, "PAYU_LATAM", None)

# List of settings that have a default when a value is not provided by the user.
DEFAULTS = {
    'API_LOGIN': None,
    'API_KEY': None,
    'MERCHANT_ID': None,
    'ACCOUNT_ID': None,
}

# List of settings that cannot be empty
MANDATORY = (
    'API_LOGIN',
    'API_KEY',
    'MERCHANT_ID',
    'ACCOUNT_ID',
)


class PayULatamSettings(object):
    """
        Settings object that allows accessing the PayU Latam settings as properties.
    """

    def __init__(self, user_settings=None, defaults=None, mandatory=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.mandatory = mandatory or {}

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid PayU Latam setting: %r" % (attr))

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        self.validate_setting(attr, val)

        # Cache the result
        setattr(self, attr, val)
        return val

    def validate_setting(self, attr, val):
        if not val and attr in self.mandatory:
            raise AttributeError("PayU Latam setting: %r is mandatory" % (attr))


payulatam_settings = PayULatamSettings(USER_SETTINGS, DEFAULTS, MANDATORY)
