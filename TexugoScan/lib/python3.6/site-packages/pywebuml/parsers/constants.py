# -*- codign: utf-8 -*-

'''
Has different constants used in the different parsers.

@author: tzulberti
'''

# Methods or attributes modifiers. See:
# http://msdn.microsoft.com/en-us/library/6tcf2h8w%28v=vs.71%29.aspx
# TODO order them by name
MODIFIERS = [
    "abstract",
    "const",
    "event",
    "extern",
    "delegate",
    "new",
    "internal",
    "override",
    "private",
    "protected",
    "public",
    "readonly",
    "sealed",
    "static",
    "unsafe",
    "virtual",
    "volatile",
    "final",
    "transient",
    "synchronized",
]


ABSTRACT_KEYWORDS = [
    "abstract",
    "delegate",
    "extern",
]

CLASS_KEYWORDS = [
    "class",
    "struct",
    "interface",
    "partial",
    "enum",
]

CONST_KEYWORDS = [
    "const",
    "readonly",
]

PREPROCESSOR_DIRECTIVES = [
    '#if',
    '#else',
    '#elif',
    '#endif',
    '#undef',
    '#define',
    '#warning',
    '#error',
    '#line',
    '#region',
    '#endregion',
    '#pragma',
    '#pragma warning',
    '#pragma checksum',
]


# this are preprocesor directives that doesn't
# change the logic of the file.
SIMPLE_PREPROCESSOR_DIRECTIVES = [
    '#warning',
    '#error',
    '#line',
    '#region',
    '#endregion',
    '#pragma',
    '#pragma warning',
    '#pragma checksum',
]

COMMENTS_MARKERS = [
    '//',
    '///',
    '/*',
    '/**',
    '*/',
    '*',
]

LANGUAGE_BASE_VALUES = [
    'int',
    'int?',
    'float',
    'float?',
    'double',
    'double?',
    'long',
    'long?',
    'string',
    'string?',
    'char',
    'char?',
    'bool',
    'bool?',
    'boolean',
    'object',
    'Object',
    'enum',
    'String',
    'Boolean',
    'Integer',
    'Long',
    'Double',
    'BigInt',
]


JAVA_LANGUAGE_METHODS = [
    'clone',
    'equals',
    'finalize',
    'getClass',
    'hashCode',
    'notify',
    'notifyAll',
    'toString',
    'wait',
]
