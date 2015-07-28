import requests
from contact_mapper import ObjectContactMapperFormat, JSONContactMapperFormat, ContactMapper


def compute_trust(user, tracking_data=None):
    api_data = dict()

    # Add API key
    api_data['api_key'] = api_key

    # Add user data
    from_format = ObjectContactMapperFormat
    to_format = JSONContactMapperFormat
    mapper = ContactMapper(from_format, to_format)
    api_data['user_data'] = mapper.convert(contact)

    response = requests.post(url="http://www.basset.io/trust", data=api_data)

    return response


def send_interaction(contact, transaction_type, tracking_data, api_key):
    api_data = dict()

    # Add API key
    api_data['api_key'] = api_key

    # Add user data
    from_format = ObjectContactMapperFormat
    to_format = JSONContactMapperFormat
    mapper = ContactMapper(from_format, to_format)
    api_data['user_data'] = mapper.convert(contact)

    # Add transaction type
    api_data['transaction_type'] = transaction_type

    # Add tracking data
    api_data['tracking_data'] = tracking_data

    response = requests.put(url="http://www.basset.io/interaction", data=api_data)

    return response
