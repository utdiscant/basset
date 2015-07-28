from behave import *
import requests

from contact_utils.contact_mapper import JSONContactMapperFormat, ObjectContactMapperFormat, ContactMapper
from contact import User


@given('we have the testing database')
def step_impl(context):
    pass

@when('we query the api endpoint \'{endpoint}\' with')
def step_impl(context, endpoint):
    url = "http://127.0.0.1:5000" + endpoint
    context.api_result = requests.post(url, data=context.text).text

@then('the API will return a string')
def step_impl(context):
    assert isinstance(context.api_result, unicode)






@given('we have a contact mapper from {from_format} to {to_format}')
def step_impl(context, from_format, to_format):
    from_format = ObjectContactMapperFormat()
    to_format   = JSONContactMapperFormat()
    context.mapper = ContactMapper(from_format, to_format)

@when('we input a contact in {format} format into the converter')
def step_impl(context, format):
    if format == "Contact":
        input_contact = User()
        input_contact.add_info("email", address="utdiscant@gmail.com", label="work")
        input_contact.add_info("name", givenName="David", familyName="Kofoed Wind", fullName="David Kofoed Wind")
        input_contact.add_info("organization", name="Onetact", title="CTO")
        context.input = input_contact

    context.output = context.mapper.convert(context.input)

@when('we convert it back again')
def step_impl(context):
    reverse_mapper = context.mapper.reverse_mapper()
    context.output = reverse_mapper.convert(context.output)

@then('we get the original contact back')
def step_impl(context):
    assert context.input == context.output