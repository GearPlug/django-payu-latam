import datetime

from django import forms


class PayuDateTimeField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return None
        return datetime.datetime.strptime(value, '%Y.%m.%d %H:%M:%S')
