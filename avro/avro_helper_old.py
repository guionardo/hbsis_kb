import avro_json_serializer
import avro.schema
import os
import re
import requests
import json


class AvroHelper():
    '''
    Classe Helper para serialização/deserialização de objetos    
    @author Guionardo Furlan    
    '''
    _last_exception = None
    last_schema = None
    debug = True

    @staticmethod
    def getException() -> Exception:
        '''Retorna a última exceção lançada'''
        return AvroHelper._last_exception

    @staticmethod
    def setException(e):
        '''Atualiza a última exceção lançada, imprimindo para debug'''
        if AvroHelper.debug:
            print('Exception: ', str(e))
        AvroHelper._last_exception = e

    @staticmethod
    def loadJSON(source: str) -> str:
        '''
        Carrega a informação JSON de várias mídias e devolve como string

        source pode ser uma string JSON, um nome de arquivo ou uma URL com conteúdo JSON
        '''
        try:
            # Verifica se é um arquivo existente
            print(os.getcwd())
            if (os.path.exists(source) and os.path.isfile(source)):
                with open(source, 'r') as f:
                    return f.read()

            # Verifica se é uma URL e obtém via request GET
            pattern = re.compile(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
            if (pattern.fullmatch(source)):
                return requests.get(url=source).text

            # Tenta fazer o parse do JSON (json.loads estoura caso o source seja inválido)
            json.loads(source)
            return source
        except Exception as e:
            AvroHelper.setException(e)

        return None

    @staticmethod
    def parseschema(schema, force=False) -> bool:
        '''
        Trata a informação do schema utilizado. 

        Argumento pode ser um objeto RecordSchema, ou um JSON, ou um arquivo com o conteúdo JSON, ou uma URL com o conteúdo JSON
        '''
        if ((not AvroHelper.last_schema is None) and not force):
            return True
        AvroHelper.last_schema = None
        if type(schema) is avro.schema.RecordSchema:
            AvroHelper.last_schema = schema
            return True
        if (type(schema) is str):
            try:
                schema = AvroHelper.loadJSON(schema)
                nschema = avro.schema.Parse(schema)
                AvroHelper.last_schema = nschema
                return True
            except Exception as e:
                AvroHelper.setException(e)
                return False

        return False

    @staticmethod
    def checkSchema(schema, force=False):
        '''
        Verifica se o schema informado é válido
        '''
        if (not force and not (schema is None)):
            return True
        if schema is None:
            schema = AvroHelper.last_schema
        else:
            AvroHelper.parseschema(schema)
        if (AvroHelper.last_schema is None):
            return False
            #raise Exception('Schema undefined')
        return True

    @staticmethod
    def serialize(data, schema=None):
        '''Efetua a serialização do objeto de acordo com o schema informado'''
        try:
            AvroHelper.checkSchema(schema)
            if AvroHelper.last_schema is None:
                json_str = json.dumps(data)
            else:
                serializer = avro_json_serializer.AvroJsonSerializer(
                    AvroHelper.last_schema)
                json_str = serializer.to_json(data)

            return json_str
        except Exception as e:
            AvroHelper.setException(e)
            return None

    @staticmethod
    def deserialize(cjson, schema=None):
        try:
            AvroHelper.checkSchema(schema)
            if AvroHelper.last_schema is None:
                obj = json.loads(cjson)
            else:
                deserializer = avro_json_serializer.AvroJsonDeserializer(
                    AvroHelper.last_schema)
                obj = deserializer.from_json(cjson)
            return obj
        except Exception as e:
            AvroHelper.setException(e)
            return None
