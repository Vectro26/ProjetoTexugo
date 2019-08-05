# -*- coding: utf-8 -*-

'''
Created on 05/02/2011

@author: tzulberti
'''

from pywebuml.parsers.static_typed.method_parser import AbstractStaticTypedMethodParser
from pywebuml.parsers.utils import has_any_keyword

class CSharpMethodParser(AbstractStaticTypedMethodParser):
    ''' Parser for CSharp methods.
    '''

    def clean_language_things(self, signature):
        ''' Removes the templates conditions of the method signature.
        '''
        # TODO keyword bug
        if 'where' in signature and ':' in signature and signature.index('where') > signature.index(')'):
            # take into account methods that uses templates with conditionals.
            signature = signature[:signature.index('where')].strip()
        elif ':' in signature:
            # take into account that it cant be an inline constructor.
            # for example:
            #   public MyClass(): this("foo") {}
            signature = signature[:signature.index(':')].strip()

        # check if the method is a template method. For example:
        #   T GetValues<T>(string key)
        open_parethesis = signature.index('(') -1
        should_split = False
        for position in range(open_parethesis, 0, -1):
            if signature[position] != ' ':
                if signature[position] == '>':
                    should_split = True
                break

        if should_split:
            # remove the Template name from the method name.
            end_template = position
            for start_template in range(end_template, 0, -1):
                if signature[start_template] == '<':
                    break

            signature = signature[:start_template] + signature[end_template +1:]

        return signature


    def should_skip_language_methods(self, signature):
        ''' Skip the method if it is an operator.
        '''
        return has_any_keyword(signature, ['operator'])

