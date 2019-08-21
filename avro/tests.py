import unittest
import os
import sys
import time
from avro_helper import AvroHelper


class Tests(unittest.TestCase):
    def setUp(self):
        self.dataobject = {
            'nome': 'Guionardo',
            'nascimento': '1977-02-05',
            'ativo': True,
            'hash': 'ABC\nLINHA2\nOUTRA LINHA'
        }
        plocal = str(os.getcwd())
        if not plocal.endswith('avro'):
            plocal = os.path.join(plocal, 'avro')

        self.plocal = plocal

        self.dataschema = os.path.join(plocal, 'data_schema.json')
        if not os.path.exists(self.dataschema):
            self.dataschema = os.path.join('avro', self.dataschema)
            if not os.path.exists(self.dataschema):
                raise Exception('Arquivo data_schema.json não foi encontrado')

    def testSerialize(self):
        AvroHelper.parseschema(self.dataschema)
        print(self.dataobject)
        ser = AvroHelper.serialize(self.dataobject)
        print(ser)
        self.assertIsNotNone(ser)

    def testDeserialize(self):
        AvroHelper.parseschema(self.dataschema)
        serializaded = AvroHelper.serialize(self.dataobject)
        self.assertIsNotNone(serializaded)
        self.assertIsNotNone(AvroHelper.deserialize(serializaded))

    def testJSONLoadString(self):
        json = '{"nome":"Guionardo","nascimento":"1977-02-05", "ativo": "True", "hash": "ABC"}'
        self.assertIsNotNone(AvroHelper.loadJSON(json), 'Teste source string')

    def testJSONLoadFile(self):
        self.assertIsNotNone(AvroHelper.loadJSON(
            self.dataschema), 'Teste source arquivo')

    def testJSONLoadURL(self):
        self.assertIsNotNone(AvroHelper.loadJSON(
            'https://github.com/guionardo/teste_git/raw/master/teste.json'), 'Teste source URL')

    def testSerializeSemSchema(self):
        AvroHelper.last_schema = None
        serializaded = AvroHelper.serialize(self.dataobject)
        self.assertIsNotNone(serializaded)

    def testDeserializeSemSchema(self):
        AvroHelper.last_schema = None
        serializaded = AvroHelper.serialize(self.dataobject)
        self.assertIsNotNone(serializaded)
        self.assertIsNotNone(AvroHelper.deserialize(serializaded))

    def testJSONLoadURLBig(self):
        now = time.time()
        AvroHelper.last_schema = None
        cobjeto = AvroHelper.loadJSON(
            'https://github.com/zemirco/sf-city-lots-json/raw/master/citylots.json')
        print('Download: ', len(cobjeto), ' em ', time.time()-now,
              ' = ', len(cobjeto)/(time.time()-now)/1024, 'KB/s')
        self.assertIsNotNone(cobjeto, 'Teste source URL')
        self.assertLess(time.time()-now, 30,
                        'Download de 180MB em mais de 30 segundos')
        now = time.time()
        objeto = AvroHelper.deserialize(cobjeto)
        print('Deserialização: ', time.time() - now, ' (', len(objeto), ')')
        self.assertLess(time.time()-now, 15,
                        'Deserialização em mais de 15 segundos')

    def testJSONLoadFileBig(self):
        now = time.time()
        AvroHelper.last_schema = None
        fjson = os.path.join(self.plocal, 'citylots.json')
        self.assertTrue(os.path.exists(fjson),
                        'Arquivo citylots.json inexistente.')
        cobjeto = AvroHelper.loadJSON(fjson)

        print('Leitura: ', len(cobjeto), ' em ', time.time()-now,
              ' = ', len(cobjeto)/(time.time()-now)/1024, 'KB/s')
        self.assertIsNotNone(cobjeto, 'Teste source URL')
        self.assertLess(time.time()-now, 30,
                        'Leitura de 180MB em mais de 30 segundos')
        now = time.time()
        objeto = AvroHelper.deserialize(cobjeto)
        print('Deserialização: ', time.time() - now, ' (', len(objeto), ')')
        self.assertLess(time.time()-now, 15,
                        'Deserialização em mais de 15 segundos')
