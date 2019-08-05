# -*- coding: utf-8 -*-

'''
Attribute parser for Java files.

@author: tzulberti
Created on: 13/03/2011
'''

from pywebuml.models import Enum
from pywebuml.parsers.static_typed.attribute_parser import AbstractStaticTypedAttributeParser

class JavaAttributeParser(AbstractStaticTypedAttributeParser):
    ''' Java attribute parser for the java classes.
    '''

    def should_update_index(self, current_line, content, current_position, class_model):
        if isinstance(class_model, Enum):
            if current_line.endswith(',') or \
                    current_line.endswith(';') or \
                    (not ' ' in current_line and not '(' in current_line):
                return False
        return super(JavaAttributeParser, self).should_update_index(current_line,
                            content,
                            current_position,
                            class_model)
