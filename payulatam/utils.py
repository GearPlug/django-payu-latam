import hashlib


def get_signature(api_key, merchant_id, reference_code, tx_value, currency, state_pol):
    signature = '{}~{}~{}~{}~{}~{}'.format(api_key, merchant_id, reference_code, tx_value, currency, state_pol)
    return hashlib.md5(signature.encode('utf')).hexdigest()
