import re

from scheme.exceptions import *
from scheme.fields import Field, Text
from scheme.util import construct_all_list, identify_class, import_object

class ObjectReference(Field):
    """A resource field for references to python objects."""

    errors = {
        'invalid': '%(field)s must be a python object',
        'import': '%(field)s specifies a python object which cannot be imported',
    }

    def _serialize_value(self, value):
        return identify_class(value)

    def _unserialize_value(self, value):
        if not isinstance(value, basestring):
            raise InvalidTypeError(value=value).construct(self, 'invalid')

        try:
            return import_object(value)
        except ImportError:
            raise ValidationError(value=value).construct(self, 'import')

class Url(Field):
    """A resource field for urls."""

    pattern = re.compile('(?i)'
        r'^([^:]+)://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$'
    )

__all__ = construct_all_list(locals(), Field)
