# Methods for converting between various contact formats
from contact_utils import Contact, Info
from contact_utils.exceptions import ContactConversionException

#    from_format = ObjectContactMapperFormat #ContactMapperFormat(from_format)
#    to_format   = JSONContactMapperFormat #(to_format)
#    context.mapper = ContactMapper(from_format, to_format)


class ContactMapper():
    def __init__(self, input_format, output_format):
        self.input_format = input_format()
        self.output_format = output_format()

    def convert(self, input_data):
        try:
            contact_object = self.input_format.to_contact_object(input_data)
            return self.output_format.from_contact_object(contact_object)
        except:
            raise ContactConversionException

    def reverse_mapper(self):
        return ContactMapper(input_format=self.output_format, output_format=self.input_format)


class ContactMapperFormat():
    def __init__(self):
        pass


class ObjectContactMapperFormat(ContactMapperFormat):
    def to_contact_object(self, input_data):
        return input_data

    def from_contact_object(self, input_data):
        return input_data


class GraphContactMapperFormat(ContactMapperFormat):
    def to_contact_object(self, graph_object):
        resulting_contact = Contact()

        def extract_node_info_type(node):
            labels = node.labels
            info_types = Info.TYPES
            return filter(lambda l: l in info_types, labels)[0]

        for node in graph_object.nodes:
            if "info" in node.labels:
                resulting_contact.add_info(info_type=extract_node_info_type(node), **node.properties)
        return resulting_contact

    def from_contact_object(self, contact_object):
        raise NotImplementedError


class JSONContactMapperFormat(ContactMapperFormat):
    def to_contact_object(self, json_contact):
        contact_object = Contact(**json_contact)
        return contact_object

    def from_contact_object(self, contact_object):
        json_contact = dict()
        json_contact['flags'] = contact_object.flags

        def recursive_to_dict(something):
            if isinstance(something, list):
                return map(recursive_to_dict, something)
            elif isinstance(something, dict):
                return {key: recursive_to_dict(value) for key, value in something.items()}
            elif isinstance(something, Info):
                return something.to_dict()
            else:
                return something

        json_contact.update(recursive_to_dict(contact_object.info))

        return json_contact
