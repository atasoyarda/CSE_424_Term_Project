from Crypto.Hash import SHA256
import json
import jsonpickle

class BlockchainUtils:

    @classmethod
    def hash(cls, data):
        return SHA256.new(json.dumps(data).encode('utf-8'))

    @classmethod
    def encode(cls, objectToEncode):
        return jsonpickle.encode(objectToEncode, unpicklable=True)

    @classmethod
    def decode(cls, encodedObject):
        return jsonpickle.decode(encodedObject)