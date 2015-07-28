import copy


class Info():
    TYPES = ['name',
             'email',
             'phone',
             'address',
             'organization',
             'custom',
             'photo']

    CONSTRAINTS = {'name': ['given_name', 'family_name', 'full_name'],
                   'phone': ['country_code', 'number', 'label'],
                   'email': ['address', 'label'],
                   'address': ['address', 'label'],
                   'organization': ['title', 'org_name']}

    def __init__(self, **kwargs):
        self.info_type = kwargs.pop('type', None)
        if self.info_type is None:
            raise TypeError('Info type not provided')
        if self.info_type not in Info.TYPES:
            raise TypeError(self.info_type + ' is not a valid Info type')

        sanitized_kwargs = self.sanitize(kwargs)
        for key, value in sanitized_kwargs.items():
            if self.info_type in Info.CONSTRAINTS and key not in Info.CONSTRAINTS[self.info_type]:
                raise KeyError("'%s' is not allowed for info type '%s'" % (key, self.info_type))
            if value is None or value == "":
                pass
                # raise ValueError('Empty info value provided') #TODO!
            else:
                setattr(self, key, value)

    def sanitize(self, info_dict):
        if 'label' in info_dict:
            info_dict['label'] = info_dict['label'].title().strip() # Title Casing
            if info_dict['label'] == 'Home':
                info_dict['label'] = 'Private'

        if 'data' in info_dict:
            del info_dict['data']
            # TODO: make hash

        if 'key' in info_dict:
            info_dict['key'] = info_dict['key'].lower().replace(" ", "_").replace(".", "_")

        if self.info_type == 'email':
            info_dict['address'] = info_dict['address'].lower()

        if self.info_type == 'phone':
            info_dict['number'] = info_dict['number'].replace(" ", "")

        return info_dict

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self):
        as_dict = copy.deepcopy(self.__dict__)
        return as_dict