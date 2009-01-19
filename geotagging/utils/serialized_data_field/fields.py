#http://www.davidcramer.net/code/181/custom-fields-in-django.html

from django.db import models
 
try:
    import cPickle as pickle
except:
    import pickle
 
import base64
 
class SerializedDataField(models.TextField):
    """Because Django for some reason feels its needed to repeatedly call
    to_python even after it's been converted this does not support strings."""
    __metaclass__ = models.SubfieldBase
 
    def to_python(self, value):
        if value is None: 
            return
        if not isinstance(value, basestring): 
            return value
        try:
            value = pickle.loads(base64.b64decode(value))
        except EOFError:
            return
        return value
 
    def get_db_prep_save(self, value):
        if value is None: 
            return
        return base64.b64encode(pickle.dumps(value))