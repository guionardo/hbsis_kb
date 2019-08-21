'''
Classe para processamento de objetos AVRO
'''
import io
import re
import requests
import os
import avro
import json
import tempfile
from avro import schema as Schema
from avro.io import DatumReader, DatumWriter
from avro.datafile import DataFileReader, DataFileWriter
import avro_json_serializer


class AvroObject():

    def __init__(self):
        self._data = {'schema': None,
                      'data': None,
                      'namespace': None,
                      'type': None,
                      'name': None,
                      'origin': None}

    def getSchemaInfos(self):
        '''
        Retorna dict com informações sobre o último schema utilizado
        '''
        return {
            "namespace": self.namespace,
            "type": self.type,
            "name": self.name,
            "origin": self.origin
        }

    def Parse(self, data, schema=None) -> tuple:
        '''
        Trata informações e gera o objeto
        A tupla de retorno tem dois valores (Sucesso: bool, Mensagem: str)
        '''
        if type(data) is bytes:
            return self._parsebytes(data, schema)
        elif type(data) is str:
            return self._parsestr(data, schema)
        return (False, 'Paramêtro inválido')

    @staticmethod
    def FetchJSON(source: str) -> tuple:
        '''Carrega a informação JSON de várias mídias e devolve como string

        source pode ser uma string JSON, nome de arquivo, URL

        retorna uma tupla (Sucesso, conteúdo ou mensagem de erro, origem)
        '''
        try:
            # Verifica se é um arquivo existente
            if(os.path.exists(source) and os.path.isfile(source)):
                with open(source, 'r') as f:
                    content = f.read()
                    f.close()
                    return (True, content, os.path.abspath(source))

            # Verifica se é uma URL
            pattern = re.compile(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
            if (pattern.fullmatch(source)):
                content = requests.get(url=source).text
                return (True, content, source)

            # Tenta fazer o parse do JSON (json.loads estoura caso o source seja inválido)
            json.loads(source)
            return (True, source, "string")
        except Exception as e:
            return (True, str(e), None)

    def ExportToText(self, data, schema=None) -> tuple:
        '''
        Exporta objeto data utilizando o schema informado em formato texto (JSON)
        '''
        if not schema == None:
            if (self._parseschema(schema)):
                schema = self._data['schema']
        else:
            schema = self._data['schema']

        try:
            if schema is None:
                export_json = json.dumps(data)
            else:
                serializer = avro_json_serializer.AvroJsonSerializer(schema)
                export_json = serializer.to_json(data)

            return (True, export_json, self.getSchemaInfos())
        except Exception as e:
            return (False, str(e), self.getSchemaInfos())

    def ExportToBin(self, data, schema=None) -> tuple:
        '''
        Exporta objeto data utilizando o schema informado em formato binário (bytes)
        '''
        if not schema == None:
            pschema = self._parseschema(schema)
            if pschema[0]:
                schema = self._data['schema']
            else:
                return pschema

        else:
            schema = self._data['schema']

        if not type(schema) is avro.schema.RecordSchema:
            schema = None
        try:
            with tempfile.SpooledTemporaryFile(suffix='.avro') as tmp:
                writer = DataFileWriter(tmp, DatumWriter(), schema)
                if not data is list:
                    writer.append(data)
                else:
                    for d in data:
                        writer.append(d)
                writer.flush()
                tmp.seek(0)
                export_bin = tmp.read()
                writer.close()
                tmp.close()
                self._data['data'] = export_bin
            return (True, export_bin, self.getSchemaInfos())
        except Exception as e:
            return (False, str(e), self.getSchemaInfos())

    def _parsebytes(self, data, schema) -> tuple:
        '''Trata informações a partir de dados bytes'''
        try:
            bdata = io.BytesIO(data)
            reader = DataFileReader(bdata, DatumReader())
            cschema = reader.GetMeta('avro.schema')
            obj_data = []
            for datum in reader:
                obj_data.append(datum)

            reader.close()
            self._data['schema'] = cschema
            self._data['data'] = obj_data
            self._data['origin'] = ('binary', None)
            return (True, 'OK')
        except Exception as e:
            return (False, str(e))

    def _parsestr(self, data, schema) -> tuple:
        '''Trata informações a partir de uma string json'''
        f = AvroObject.FetchJSON(data)
        if (not f[0]):  # Erro no fetch da informação
            return (False, f[1])

        data = f[1]
        try:
            if (not schema is None):
                self._parseschema(schema)

            if type(self._data['schema']) is avro.schema.RecordSchema:
                deserializer = avro_json_serializer.AvroJsonDeserializer(
                    self._data['schema'])
                obj = deserializer.from_json(data)
            else:
                obj = json.loads(data)

            self._data['data'] = obj
            self._data['origin'] = ('text', f[2])
            return (True, 'OK')
        except Exception as e:
            return (False, str(e))

        return (False, 'Parâmetro inválido')

    def _parsefile(self, data, schema) -> tuple:
        '''Trata informações lidas a partir de um arquivo'''

        # Detectar se é um arquivo binário ou um texto com JSON
        try:
            binary = False
            filename = os.path.abspath(data)
            with open(filename, 'rb') as f:
                if f.read(3) == b'Obj':
                    # Arquivo binário
                    f.seek(0)
                    data = f.read()
                    binary = True
                f.close()
            if not binary:
                with open(data, 'r') as f:
                    data = f.read()
                    f.close()
            if binary:
                ret = self._parsebytes(data, schema)
                self._data['origin'] = ('file/binary:', filename)
            else:
                ret = self._parsestr(data, schema)
                self._data['origin'] = ('file/text:', filename)
            return ret

        except Exception as e:
            return (False, str(e))

        return (False, 'Parâmetro inválido')

    def _parseschema(self, schema) -> tuple:
        '''Carrega a informação de um schema

        Argumento pode ser um objeto RecordSchema, um dict, um JSON, ou um arquivo com o conteúdo JSON, ou uma URL com o conteúdo JSON'''

        if type(schema) is dict:
            schema = json.dumps(schema)

        if type(schema) is str:
            try:
                fetch = AvroObject.FetchJSON(schema)
                if (fetch[0]):
                    schema = fetch[1]
                else:
                    return (False, fetch[1])

                schema = avro.schema.Parse(schema)
            except Exception as e:
                return (False, str(e))

        if type(schema) is avro.schema.RecordSchema:
            self._data['schema'] = schema
            return (True, 'OK')

        return (False, 'NO SCHEMA')

    def __getattr__(self, name: str):
        name = name.lower()

        if name == 'schema':
            if (self._data['schema'] is None):
                # Não há informação de schema definida
                return None
            elif (type(self._data['schema']) in [str, bytes]):
                try:
                    jschema = avro.schema.Parse(self._data['schema'])
                    self._data['schema'] = jschema
                except:
                    return None

            if (type(self._data['schema']) is avro.schema.RecordSchema):
                # O schema já foi lido anterimente
                return self._data['schema']

            return None

        if not (name in ['namespace', 'name', 'type', 'schema', 'data', 'origin']):
            raise AttributeError(name)

        if (self._data[name] is None):
            jschema = self.schema
            if not (jschema is None):
                if (name == 'namespace'):
                    self._data['namespace'] = jschema.namespace
                elif (name == 'name'):
                    self._data['name'] = jschema.name
                elif (name == 'type'):
                    self._data['type'] = jschema.type

            else:
                self._data[name] = None

        return self._data[name]


def avro_object_to_bin(data, schema) -> tuple:
    '''
    Converte um objeto em um formato binário a partir do schema

    retorna uma tupla (Sucesso, binário ou mensagem de erro)
    '''
    ao = AvroObject()
    return ao.ExportToBin(data, schema)


def avro_object_to_json(data, schema=None) -> tuple:
    '''
    Converte um objeto em seu formato json a partir do schema (opcional)

    retorna uma tupla (Sucesso, string json ou mensagem de erro)
    '''
    ao = AvroObject()
    return ao.ExportToText(data, schema)


def avro_bin_to_object(bin_data) -> tuple:
    '''
    Converte um binário em seu objeto. O schema já deve estar embutido no binário

    retorna uma tupla (Sucesso, objeto ou mensagem de erro)
    '''
    ao = AvroObject()
    return (ao.Parse(bin_data)[0], ao.data, ao.getSchemaInfos())


def avro_json_to_object(json_data, schema) -> tuple:
    '''
    Converte um string em um objeto a partir do schema (obrigatório)

    retorna uma tupla (Sucesso, objeto ou mensagem de erro)
    '''
    ao = AvroObject()
    ret = ao.Parse(json_data, schema)
    if ret[0]:
        return (True, ao.data)
    else:
        return ret
