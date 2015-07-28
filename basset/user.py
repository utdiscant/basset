from functools import partial
import copy

from info import Info


class User():
    """
    This class represents a contact

    * The structure that is kind of expected (not yet inforced):
      * name (non-empty dict)
        * givenName (string)
        * familyName (string)
        * fullName (string)
      * email (non-empty list of non-empy dicts)
        * email_address (string)
        * label (string)
      * phone
        * country_code (string)
        * number (string)
        * label (string)
      * postal
        * postal_address (string)
        * label (string)
      * custom
        * key (string)
        * value (string)
    """

    def __init__(self, **kwargs):
        self.info = {}

        if kwargs:
            self.__add_info_from_kwargs(**kwargs)

        # Syntactic sugar
        # ---------------
        # This adds adder-methods like add_organization(**kwargs)
        '''
        for info_type in Info.TYPES:
            setattr(self, 'add_' + info_type, partial(self.add_info, type=info_type))

        # This adds getter-methods like get_organization()
        for info_type in Info.TYPES:
            setattr(self, 'get_' + info_type, partial(self.get_info, type=info_type))

        # This adds exists-methods like has_organization()
        for info_type in Info.TYPES:
            setattr(self, 'has_' + info_type, partial(self.has_info, type=info_type))
        '''

    def __eq__(self, other):
        for info in self:
            if info not in other:
                return False
        return True

    def __str__(self):
        result_string = ""
        for info_type in self.info:
            result_string += info_type + "\n"
            for info_elem in self.info[info_type]:
                result_string += "   " + str(info_elem) + "\n"
        return result_string

    def add_info(self, info_type, **kwargs):
        info_instance = Info(type=info_type, **kwargs)
        self.__add_info_instance(info_instance)
        return info_instance

    def add_name(self, given_name=None, family_name=None, full_name=None):
        print "HERE"
        return self.add_info(info_type="name", given_name=given_name, family_name=family_name, full_name=full_name)

    def add_email(self, address=None):
        return self.add_info(info_type="email", address=address)

    def add_social_profile(self, handle=None, site=None):
        return self.add_info(info_type="social_profile", handle=handle, site=site)

    def add_phone(self, number=None, country=None):
        return self.add_info(info_type="phone", number=number, country=country)

    def add_postal_address(self, postal_address=None):
        return self.add_info(info_type="postal_address", postal_address=postal_address)

    def add_credit_card(self, cardno=None):
        return self.add_info(info_type="credit_card", cardno=cardno)

    def get_info(self, info_type):
        if info_type not in Info.TYPES:
            raise TypeError('The following Info type is not supported: ' + info_type)
        if not self.has_info(info_type):
            return None
        else:
            return self.info[info_type]

    def has_info(self, info_type):
        return info_type in self.info

    def update(self, other_contact):
        other_copy = copy.deepcopy(other_contact)
        self.__add_info_instance(other_copy.info.values())

    def __iter__(self):
        for info_type in self.info:
            for info in self.info[info_type]:
                yield info

    def __add_info_instance(self, new_info_obj):
        """
        An info should never be added without going through this method
        """
        # Recurse if this object is a list
        if isinstance(new_info_obj, list):
            for new_info in new_info_obj:
                self.__add_info_instance(new_info)
        else:
            # # Maintain the mapping from references to Info objects
            # self.info_references[str(new_info_obj.reference)] = new_info_obj
            # Append to the proper list (create the list if necessary)
            info_type = new_info_obj.info_type
            if info_type in self.info:
                if new_info_obj in self.info[info_type]:
                    index = self.info[info_type].index(new_info_obj)
                    self.info[info_type][index].update(new_info_obj)
                else:
                    self.info[info_type].append(new_info_obj)
            else:
                self.info[info_type] = [new_info_obj]

    def __add_info_from_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key in Info.TYPES:
                info_instance = self.__make_info_instance(key, value)
                self.__add_info_instance(info_instance)
            else:
                raise TypeError("We have not thought about this info_type %s" % key)

    def __make_info_instance(self, key, value):
        if isinstance(value, list):
            return [self.__make_info_instance(key, v) for v in value]
        else:
            res = Info(**value)
            return res
