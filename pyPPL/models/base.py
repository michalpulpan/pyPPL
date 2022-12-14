from collections import OrderedDict
from enum import Enum
import json
import xmltodict

class SerializableObject:
    
    def to_dict(self):
        """
        Convert object to JSON
        """
        # class_dict = {self.xml_mapping.get(k, k): v if not isinstance(v, SerializableObject) else self.xml_mapping[k].to_dict(v) for k, v in self.__dict__.items()}
        
        # ordered dict is required since xs:sequence is ordered
        class_dict = OrderedDict()
        
        if self.xml_mapping is None:
            raise NotImplementedError(f'xml_mapping is not defined {self.__class__.__name__}')

        for k, v in self.xml_mapping.items():
            if k not in self.__dict__ or self.__dict__[k] is None:
                continue

            if isinstance(v, SerializerField) and isinstance(self.__dict__[k], SerializableObject):
                class_dict[v.name] = v.to_dict(self.__dict__[k])
            elif isinstance(v, SerializerList):
                class_dict[v.name] = v.to_dict(self.__dict__[k])
            else:
                class_dict[v.name] = self.__dict__[k]
        return class_dict

        # for k, v in self.__dict__.items():
        #     if k not in self.xml_mapping:
        #         continue
        #     if isinstance(self.xml_mapping[k], SerializerField) and isinstance(v, SerializableObject):
        #         class_dict[self.xml_mapping[k].name] = self.xml_mapping[k].to_dict(v)
        #     elif isinstance(self.xml_mapping[k], SerializerList):
        #         class_dict[self.xml_mapping[k].name] = self.xml_mapping[k].to_dict(v)#v.to_dict(v)
        #     else:
        #         class_dict[self.xml_mapping[k].name] = v
        # return class_dict

    def to_xml(self):
        """
        Convert class to XML
        uses predefined xml_mapping (OrderedDict) to map class attributes to XML elements
        """
        
        if self.xml_mapping is None:
            raise NotImplementedError('xml_mapping is not defined')
        
        # ordered dict is required since xs:sequence is ordered
        json_dict = OrderedDict()
        for k, v in self.xml_mapping.items():
            if k not in self.__dict__ or self.__dict__[k] is None:
                continue

            if isinstance(v, SerializerField) and isinstance(self.__dict__[k], SerializableObject):
                json_dict[v.name] = v.to_dict(self.__dict__[k])
            elif isinstance(v, SerializerList):
                json_dict[v.name] = v.to_dict(self.__dict__[k])
            else:
                json_dict[v.name] = self.__dict__[k]
        
        # for k, v in self.__dict__.items():
        #     if k not in self.xml_mapping:
        #         continue
        #     if isinstance(self.xml_mapping[k], SerializerField) and isinstance(v, SerializableObject):
        #         json_dict[self.xml_mapping[k].name] = self.xml_mapping[k].to_dict(v)
        #     elif isinstance(self.xml_mapping[k], SerializerList):
        #         json_dict[self.xml_mapping[k].name] = self.xml_mapping[k].to_dict(v)#v.to_dict(v)
        #     else:
        #         json_dict[self.xml_mapping[k].name] = v


        # json_dict = {self.xml_mapping.get(k, k): v if not isinstance(v, SerializableObject) else v.to_dict() for k, v in self.__dict__.items()}
        # return json_dict
        # json_dict = json.dumps(json_dict)

        return xmltodict.unparse(json_dict, pretty=True, full_document=False)


class MappingType(Enum):
    """
    XML mapping type
    """
    List = 'List'
    Field = 'Field'
    Object = 'Object'


class SerializerItem:
    """
    Serializer item
    """
    def __init__(self, name: str, type: MappingType, mapping: str = None, class_type: SerializableObject = None):
        self.name = name
        self.type = type
        self.mapping = mapping
        self.class_type = class_type


class SerializerField(SerializerItem):
    """
    Serializer list
    """
    def __init__(self, name: str ):
        super().__init__(name, MappingType.Field)

    def to_dict(self, object_to_serialize: SerializableObject = None):
        """
        Convert field to JSON
        """
        print(f'SERIALIZER FIELD {self.name}')
        return object_to_serialize.to_dict()


class SerializerList(SerializerItem):
    """
    Serializer list
    """
    def __init__(self, name: str, list_item_name: str):
        super().__init__(name, MappingType.List)
        print(f'SERIALIZER LIST INIT {self.name}')
        self.list_item_name = list_item_name

    def to_dict(self, list_to_serialize: list[SerializableObject] = None):
        """
        Convert list to JSON
        """
        print(f'SERIALIZER LIST {self.name}')
        return {self.list_item_name: [item.to_dict() for item in list_to_serialize]}
        # out = []
        # for item in list_to_serialize:
            # out.append({self.list_item_name: item.to_dict()})
        # return {self.name: [{self.list_item_name: { item.to_dict() }} for item in list_to_serialize]}
        