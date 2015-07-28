import requests
import basset
from contact_mapper import ObjectUserMapperFormat, JSONUserMapperFormat, UserMapper

api_domain = "http://api.basset.io"

def compute_trust(user, tracking_data=None):
    api_data = dict()

    # Add API key
    if basset.apikey is None:
        print "You need to set the API key first"
        return None
    else:
        api_data['api_key'] = basset.apikey

    # Add user data
    from_format = ObjectUserMapperFormat
    to_format = JSONUserMapperFormat
    mapper = UserMapper(from_format, to_format)
    api_data['user_data'] = mapper.convert(user)

    # Add tracking data if we have any
    if tracking_data is not None:
        api_data['tracking_data'] = tracking_data

    response = requests.post(url=api_domain + "/trust", data=api_data)
    print "Response"
    print response

    result = response.json()
    print "Result"
    print result

    # Work with response
    # Check the status
    # Did you have a valid API key?
    # Did you get a yes or a no?

    return response
