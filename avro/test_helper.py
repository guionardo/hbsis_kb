from avro_helper2 import AvroObject, avro_object_to_bin, avro_object_to_json, avro_bin_to_object, avro_json_to_object
import unittest
import json


class AvroHelperTest(unittest.TestCase):

    def setUp(self):
        self.cschema = '''{"namespace":"org.apache.avro.ipc",
        "type": "record",
        "name": "User",
        "fields": [
            {"name":"nome", "type":"string"},
            {"name":"idade", "type":"int"}
        ]}'''
        self.oschema = {"namespace": "org.apache.avro.ipc",
                        "type": "record",
                        "name": "User",
                        "fields": [
                            {"name": "nome", "type": "string"},
                            {"name": "idade", "type": "int"}
                        ]}

        self.obj1 = {"nome": "Guionardo", "idade": 42}
        self.obj2 = {"nome": "Marines", "Idade": 42}

    def test_schema_string(self):
        ao = AvroObject()        
        self.assertTrue(ao._parseschema(self.cschema)[0])

    def test_schema_object(self):
        ao = AvroObject()
        self.assertTrue(ao._parseschema(self.oschema)[0])

    def test_export_object(self):
        ret = avro_object_to_bin(self.obj1, self.oschema)
        print(ret)
        self.assertTrue(ret[0])
        ret = avro_object_to_bin(self.obj2, self.oschema)
        print(ret)
        self.assertFalse(ret[0])

    def test_export_text(self):
        ret = avro_object_to_json(self.obj1, self.oschema)
        print(ret)
        self.assertTrue(ret[0])
        ret = avro_object_to_json(self.obj2, self.oschema)
        print(ret)
        self.assertFalse(ret[0])

    def test_parse_object_file(self):
        ret = avro_bin_to_object('avro/users.avro')
        print(ret)
        self.assertTrue(ret[0])

    def test_parse_text(self):
        ret = avro_json_to_object(json.dumps(self.obj1), self.oschema)
        print(ret)
        self.assertTrue(ret[0])
        ret = avro_json_to_object(json.dumps(self.obj2), self.oschema)
        print(ret)
        self.assertFalse(ret[0])
