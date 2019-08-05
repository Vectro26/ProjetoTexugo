# -*- coding: utf-8 -*-

'''
Created on 12/03/2011

@author: tzulberti
'''
from logging import getLogger

from pywebuml.models import Method, Interface
from pywebuml.parsers.exceptions import (
                    MissingClosingParenthesis,
                    MissingClosingMethod,
                    )
from pywebuml.parsers.utils import (
                    get_visibility,
                    remove_keywords,
                    has_any_keyword,
                    get_type_and_name,
                    )
from pywebuml.parsers.constants import (
                    ABSTRACT_KEYWORDS,
                    MODIFIERS,
                    )

LOGGER = getLogger(__name__)


class AbstractStaticTypedMethodParser(object):
    ''' Abstract parser for methods.

    Given the content of the cleaned file, and a start position
    that is a method, it will have the resposability of parsing it.
    It has 2 abstract methods:

    - clean_language_things: removes specific language things from
      the method signature.

    - should_skip_language_methods: indicates if the method should
      be skipped becuase it is a language method.
    '''


    def parse(self, class_model, content, index):
        ''' Parse the method of the class of the content.

        :parameters:
            class_model:  ``pywebuml.model.Class``
                the current class that is being parsed.
            content: list(str)
                the content of the file
            index: int
                from where start parsing

        :return:
            a tuple (pywembuml.models.Method, int) that has the parsed
            method and the index value from where it should continue reading.

        :raises:
        - MissingClosingParenthesis: if it cant find the closing ) of
                                         the method signature

        '''
        current_position = index
        current_line = content[index]


        visibility = get_visibility(current_line)
        is_static = has_any_keyword(current_line, ['static'])
        is_abstract = has_any_keyword(current_line, ABSTRACT_KEYWORDS) \
                        or isinstance(class_model, Interface)

        current_line = remove_keywords(current_line, [visibility])
        current_line = remove_keywords(current_line, MODIFIERS)

        signature = current_line.strip()
        if not ')' in current_line:
            # in this case the signature of the method is in only one
            # line. For example:
            #   public void Foo(int a, int b, int c,
            #                   int d)
            current_position += 1
            while True:

                if current_position >= len(content):
                    raise MissingClosingParenthesis(index)

                signature += content[current_position].strip()
                if ')' in content[current_position]:
                    break
                current_position += 1



        if not is_abstract:
            # now move the index to the end of the method code
            # the abstract method only have thier definitions, so this
            # isn't necessary

            # take into account that the definition of the method can
            # only be of one line.
            if '{' in content[current_position] and \
                    (content[current_position].count('{') ==
                            content[current_position].count('}')):
                current_position += 1
            else:
                opened_keys = 0
                if '{' in content[current_position]:
                    opened_keys = 1

                started_method = False
                current_position += 1
                while True:
                    if current_position == len(content):
                        raise MissingClosingMethod(index)

                    line = content[current_position]
                    started_method = started_method or opened_keys > 0
                    opened_keys = opened_keys + line.count('{') - line.count('}')
                    current_position += 1
                    # take into account that the next line of the method definition
                    # could be another thing that isn't the openin. For example:
                    #   public Foo()
                    #       : base(1)
                    #   {
                    #       // do something
                    #   }
                    if opened_keys == 0 and started_method:
                        break
        else:
            current_position += 1

        # remove all the code of the signature
        if '{' in signature:
            signature = signature[:signature.index('{')].strip()


        signature = self.clean_language_things(signature)

        if self.should_skip_language_methods(signature):
            return (current_position, None)

        # remove the parameters of the signature
        tmp = signature[:signature.index('(')].strip()
        if len(tmp.split(' ')) == 1:
            # the the method is a constructor, and the name
            # is the value
            name = tmp
            return_type = 'void'
        else:
            return_type, name = get_type_and_name(tmp, index, class_model)


        LOGGER.debug("Found method: %s", name)
        return (current_position,
                Method(name, class_model, signature, visibility,
                       is_static, is_abstract),
                )


    def clean_language_things(self, signature):
        ''' Remove things of the signature that are specific for the language.
        For example, in C#:

            public T foo() where T : ....

        :parameters:
            signature: str
                the current signature of the method

        :return:
            the signature without the specific language things.
        '''
        raise NotImplementedError('clean_language_things')


    def should_skip_language_methods(self, signature):
        ''' Indicates if the method is something of the language, and
        because of that it should be skipped.

        For example, in C#::

            public bool operator !=

        :parameters:
            signature: str
                the current cleaned signature of the method

        :returns:
            True if the method should be skipped, False if the method
            should be parsed.
        '''
        raise NotImplementedError('should_skip_language_methods')



