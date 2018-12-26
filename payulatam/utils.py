import hashlib


def get_signature(api_key, merchant_id, reference_code, tx_value, currency, state_pol=None):
    """
        Genera el signature requerido por PayU al crear y verificar una transacción.
        El state_pol solo es necesario para confirmar la transacción.
    """
    if state_pol:
        signature = '{}~{}~{}~{}~{}~{}'.format(api_key, merchant_id, reference_code, tx_value, currency, state_pol)
    else:
        signature = '{}~{}~{}~{}~{}'.format(api_key, merchant_id, reference_code, tx_value, currency)
    return hashlib.md5(signature.encode('utf')).hexdigest()
