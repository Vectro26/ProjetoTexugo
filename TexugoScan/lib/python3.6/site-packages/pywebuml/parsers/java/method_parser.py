# -*- coding: utf-8 -*-

'''
@author: tzulberti
Created on 13/03/2011
'''

from pywebuml.parsers.static_typed.method_parser import AbstractStaticTypedMethodParser
from pywebuml.parsers.constants import JAVA_LANGUAGE_METHODS
from pywebuml.parsers.utils import has_any_keyword

class JavaMethodParser(AbstractStaticTypedMethodParser):
    ''' Parser for java methods.
    '''

    def clean_language_things(self, signature):
        ''' Doesn't changes the signature.
        '''
        return signature

    def should_skip_language_methods(self, signature):
        ''' Skip all the methods that belong to the Java Object methods.
        '''
        if '(' in signature:
            # remove the params of the signature just to be sure, an take
            # into account that the keywords doesn't have (. Because
            # of this it won't find:
            #       public String toString()
            signature = signature[:signature.index('(')]
        return has_any_keyword(signature, JAVA_LANGUAGE_METHODS)
