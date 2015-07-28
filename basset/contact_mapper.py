# Methods for converting between various contact formats
from user import User, Info
from exceptions import UserConversionException


class UserMapper():
    def __init__(self, input_format, output_format):
        self.input_format = input_format()
        self.output_format = output_format()

    def convert(self, input_data):
        try:
            user_object = self.input_format.to_user_object(input_data)
            return self.output_format.from_user_object(user_object)
        except:
            raise UserConversionException

    def reverse_mapper(self):
        return UserMapper(input_format=self.output_format, output_format=self.input_format)


class UserMapperFormat():
    def __init__(self):
        pass


class ObjectUserMapperFormat(UserMapperFormat):
    @staticmethod
    def to_user_object(input_data):
        return input_data

    @staticmethod
    def from_user_object(input_data):
        return input_data


class GraphUserMapperFormat(UserMapperFormat):
    @staticmethod
    def to_user_object(graph_object):
        resulting_user = User()

        def extract_node_info_type(info_node):
            labels = info_node.labels
            info_types = Info.TYPES
            return filter(lambda l: l in info_types, labels)[0]

        for node in graph_object.nodes:
            if "info" in node.labels:
                resulting_user.add_info(info_type=extract_node_info_type(node), **node.properties)
        return resulting_user

    @staticmethod
    def from_user_object(user_object):
        raise NotImplementedError


class JSONUserMapperFormat(UserMapperFormat):
    @staticmethod
    def to_user_object(json_user):
        user_object = User(**json_user)
        return user_object

    @staticmethod
    def from_user_object(user_object):
        json_user = dict()
        json_user['flags'] = user_object.flags

        def recursive_to_dict(something):
            if isinstance(something, list):
                return map(recursive_to_dict, something)
            elif isinstance(something, dict):
                return {key: recursive_to_dict(value) for key, value in something.items()}
            elif isinstance(something, Info):
                return something.to_dict()
            else:
                return something

        json_user.update(recursive_to_dict(user_object.info))

        return json_user
