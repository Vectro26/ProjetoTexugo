# -*- coding: utf-8 -*-

'''
Attribute parser for C#.

@author: tzulberti
'''

from logging import getLogger

from pywebuml.parsers.static_typed.attribute_parser import AbstractStaticTypedAttributeParser

LOGGER = getLogger(__name__)


class CSharpAttributeParser(AbstractStaticTypedAttributeParser):
    ''' Attribute parser for C# classes.
    '''


    def clean_line(self, current_line):
        ''' Adds the option of removing the property definition
        of the line if there is any.
        '''
        res = super(CSharpAttributeParser, self).clean_line(current_line)
        if '{' in res:
            res = res[0:res.index('{')]
            res = res.strip()
        return res


    def should_skip_language_attributes(self, current_line):
        ''' Skip the attributes that indicates that the class can be
        indexed.
        '''
        return 'this' in current_line or 'this [' in current_line

