import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter, BinaryEncoder, BinaryDecoder
import io, tempfile, os, json

json.loads
datum = [
    {"name": "Alyssa", "favorite_number": 256},
    {"name": "Ben", "favorite_number": 7, "favorite_color": "red"},
    {"name": "Guionardo", "favorite_color": "green"}
]

sc = avro.schema.Parse(open("avro/user.avsc", "rb").read())

def objToBin():    
    bytes_writer = io.BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer_binary = DatumWriter(sc)
    for d in datum:
        writer_binary.write(d, encoder)

    ab = bytes_writer.getvalue()
    return ab

def objToBinTmp():
    tmp = tempfile.NamedTemporaryFile(suffix='.avro',delete=False)
    tmp_fn = tmp.name    
    
    writer = DataFileWriter(tmp, DatumWriter(), sc)
    for d in datum:
        writer.append(d)    
    writer.close()
    tmp.close()

    with open(tmp_fn,'rb') as tmp_r:
        ab = tmp_r.read()
        tmp_r.close()

    os.remove(tmp_fn)
    return ab

def objToBinTmp2():
    with tempfile.SpooledTemporaryFile(suffix='.avro') as tmp:
        writer = DataFileWriter(tmp, DatumWriter(), sc)
        for d in datum:
            writer.append(d)
        writer.flush()
        tmp.seek(0)
        ab = tmp.read()
        writer.close()
        tmp.close()

    return ab

def objToBin2():    
    file = io.BytesIO()
    datum_writer = DatumWriter()
    fwriter = DataFileWriter(file, datum_writer, sc)
    for d in datum:
        fwriter.append(d)
    ab = file.getvalue()
    fwriter.close()
    
    return ab


def binToObj(ab):
    bytes_reader = io.BytesIO(ab)
    decoder = BinaryDecoder(bytes_reader)
    reader = DatumReader(sc)
    while True:
        try:
            rec = reader.read(decoder)
            print(rec)
        except:
            break

def binToObjSChema(ab):
    datum = io.BytesIO(ab)
    reader = DataFileReader(datum, DatumReader())
    cschema = reader.GetMeta('avro.schema')
    print(cschema)
    for user in reader:
        print(user)

    reader.close()


# writer = DataFileWriter(open("users.avro", "wb"), DatumWriter(), sc)
'''
writer = DataFileWriter(f,DatumWriter(), sc)
writer.append({"name": "Alyssa", "favorite_number": 256})
writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
writer.append({"name": "Guionardo", "favorite_color":"green"})
f.flush()

ab = f.getvalue()
print(ab)
ab = writer._buffer_writer.getvalue()

print(ab)

f = io.BytesIO(ab)
reader = DataFileReader(f,DatumReader())
#reader = DataFileReader(open("users.avro", "rb"), DatumReader())
for user in reader:
    print(user)
reader.close()'''

ab = objToBinTmp()
binToObjSChema(ab)

ab = objToBinTmp2()
binToObjSChema(ab)

objToBin2()

ab = objToBin()

binToObj(ab)
