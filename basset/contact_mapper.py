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

    def convert(self, input):
        try:
            contact_object = self.input_format.to_contact_object(input)
            return self.output_format.from_contact_object(contact_object)
        except:
            raise ContactConversionException

    def reverse_mapper(self):
        return ContactMapper(input_format=self.output_format, output_format=self.input_format)


class ContactMapperFormat():
    def __init__(self):
        pass


class ObjectContactMapperFormat(ContactMapperFormat):
    def to_contact_object(self, input):
        return input

    def from_contact_object(self, input):
        return input


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

# def prepare_info(info):
#     info_dict = info.to_dict()
#     del info_dict['private']
#     del info_dict['public']
#     del info_dict['flags']
#     del info_dict['reference']
#     if 'label' in info_dict:
#         del info_dict['label']
#     if 'data' in info_dict:
#         del info_dict['data']
#     return info_dict
#
#
# def to_cypher_dict(dictionary):
#     return "{" + ", ".join(["%s: '%s'" % (key, value.replace("'","")) for key, value in dictionary.items()]) + "}"
#
#
#
# class CypherContactMapperFormat():
#     def to_contact_object(self, cypher):
#         raise NotImplementedError
#
#     def from_contact_object(self, contact_object):
#         #yield "MERGE (user {email: {E}})", {"E": user.email}
#
#         yield "MERGE (contact {id:{I}})", {"I": str(personal["_id"])}
#         yield "MATCH (u:user {email:{E}}), (p:contact {id:{I}})" + \
#               "MERGE (u)-[:HAS]->(p)", \
#               {"I": str(personal["_id"]), "E": user.email}
#
#         # make contact info
#         for info in contact_object:
#             info_dict = prepare_info(info)
#             if "%s" % to_cypher_dict(info_dict) == "{}":
#                 continue
#             info_cypher = "(i:info:%s %s)" % (info.type, to_cypher_dict(info_dict))
#             yield "MERGE %s" % info_cypher,
#             yield "MATCH (p:contact {id:{I}}), %s" % info_cypher + \
#                   "MERGE (p)-[:CONTAINS]->(i)", \
#                   {"I": str(personal["_id"])}


class JSONContactMapperFormat(ContactMapperFormat):
    def to_contact_object(self, json_contact):
        contact_object = Contact(**json_contact)
        return contact_object

    def from_contact_object(self, contact_object):
        json_contact = {}
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
