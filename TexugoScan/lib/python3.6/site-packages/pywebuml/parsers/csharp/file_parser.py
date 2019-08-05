# -*- coding: utf-8 -*-

'''
File C# parser.

@author: tzulberti
'''
from logging import getLogger

from pywebuml.parsers.static_typed.file_parser import AbstractStaticTypedFileParser
from pywebuml.parsers.csharp.class_parser import CSharpClassParser
from pywebuml.parsers.constants import (
                    PREPROCESSOR_DIRECTIVES,
                    SIMPLE_PREPROCESSOR_DIRECTIVES,
                    CLASS_KEYWORDS,
                    )
from pywebuml.parsers.utils import (
                    has_any_keyword,
                    )

LOGGER = getLogger(__name__)



class CSharpFileParser(AbstractStaticTypedFileParser):
    ''' Given a C# file it will parse it's content an return
    a list of the parsed classes.
    '''

    def get_class_parser(self, content):
        return CSharpClassParser(content)


    def clean_content(self, content):
        ''' Removes all the decoratos and the code that won't
        be compiled taking into account the preprocessor directives.

        :see:
            `AbstractStaticTypeFileParser.clean_content`
        '''
        if self.has_preprocessor_directive(content):
            # take only into account the true conditions.
            content = self.remove_preprocessor_code(content)

        content = filter(lambda l : not l.startswith('['), content)
        return content


    def get_current_namespace(self, content):
        ''' Return the global namespace.
        If there is a namespace definition, then it will be updated
        in the ``should_ignore_line` method.

        :see:
            `AbstractStaticTypeFileParser.get_current_namespace`
        '''
        return 'global'


    def should_ignore_line(self, current_line, content):
        ''' Wil ignore the line if it is:
        - an import (using)
        - defines a namespace. In this case, it will update the
          current_namespace value.

        :see:
            `AbstractStaticTypeFileParser.should_ignore_line`
        '''
        if has_any_keyword(current_line, ['using']):
            self.index += 1
            return True
        elif has_any_keyword(current_line, ['namespace']):
            if not '{' in current_line:
                # if the "{" isn't in the next line, then
                # it will be in the following..
                self.index += 1
            self.index += 1
            return True
        elif '}' in current_line and not has_any_keyword(current_line, CLASS_KEYWORDS):
            # it is closing the current namespace
            self.index += 1
            return True
        else:
            return False


    def has_preprocessor_directive(self, content):
        ''' Identifies if the content of the file has a preprocesor directive.

        :parameters:
            content: list(str)
                the lines of the file.

        :returns:
            True if the file has a preprocesor directive.
        '''
        for line in content:
            if has_any_keyword(line, PREPROCESSOR_DIRECTIVES):
                return True

        return False

    def remove_preprocessor_code(self, content):
        ''' Removes the part of the content of the file
        that are code that won't be compiled taking into account the
        content of the file.

        For example in the following file::

            #define foo
            #if foo
                public class Bar {}
            #endif

        the class Bar will be returned. By if the definition of `foo` is
        commented or isn't found then an empty file might be returned.


        :parameters:
            content: list(str)
                the content read of the file. It must have a precompiler
                directive.

        :returns:
            the content of the file without any precompiler directive,
            and the actual code taking into account the definitions, if any.
        '''
        res = []
        # the names of the defined symbols
        defined = []

        # is true if any #if, #elif was true. It is used to take
        # into account that only one #if, #elif, #else can be true
        block_was_true = []


        index = 0
        while index < len(content):
            line = content[index]
            if not self._has_preprocessor_value(line, PREPROCESSOR_DIRECTIVES):
                # if there is no condition defined, then this line should
                # be added.
                res.append(line)
            else:
                # check that the preprocessor condition is one that changes
                # the code of the file.
                if not self._has_preprocessor_value(line, SIMPLE_PREPROCESSOR_DIRECTIVES):
                    is_current_block_valid = False

                    if not self._has_preprocessor_value(line, ['#else', '#endif']):
                        # all the other lines have some symbol, so I should get it
                        symbol = line[line.index(' '):]

                    if self._has_preprocessor_value(line, ['#if']):
                        is_current_block_valid = symbol in defined
                        block_was_true.append(is_current_block_valid)

                    elif self._has_preprocessor_value(line, ['#define']):
                        defined.append(symbol)
                    elif self._has_preprocessor_value(line, ['#undef']):
                        defined.remove(symbol)
                    elif self._has_preprocessor_value(line, ['#endif']):
                        block_was_true.pop()
                    elif self._has_preprocessor_value(line, ['#else']):
                        if not block_was_true[len(block_was_true) -1]:
                            # the #else condition will be true if all the #if, #elif
                            # were false.
                            block_was_true.pop()
                            block_was_true.append(True)
                            is_current_block_valid = True

                    else:
                        # the line starts with 'elif'
                        # the elif will only be used if the condition was false
                        if not block_was_true[len(block_was_true) -1]:
                            block_was_true.pop()
                            is_current_block_valid = symbol in defined
                            block_was_true.append(is_current_block_valid)

                    # will remove the lines of the blocks that aren't true
                    if self._has_preprocessor_value(line, ['#if', '#elif', '#else']) \
                            and not is_current_block_valid:
                        nested_index = index
                        unused_opened_ifs = 0
                        while nested_index < len(content):
                            nested_index += 1
                            nested_line = content[nested_index]
                            if self._has_preprocessor_value(nested_line, ['#if']):
                                unused_opened_ifs += 1
                            elif self._has_preprocessor_value(nested_line, ['#endif']) \
                                    and unused_opened_ifs > 0:
                                unused_opened_ifs -= 1
                            elif self._has_preprocessor_value(nested_line, ['#elif', '#else', '#endif']) \
                                    and unused_opened_ifs == 0:
                                # in this case a new block begins so, it should
                                # be taken into account
                                break
                        index = nested_index - 1


            index += 1

        return res




    def _has_preprocessor_value(self, line, preprocessors_to_search):
        ''' Identifies if the line has any of the preprocesosr values,
        even if they have a space.

        :parameters:
            line: str
                the current line of the file
            preprocessors_to_search: list(str)
                the list of preprocessors directives to search in the line
                it will take into account that they can have an space. They
                must have the #.
                For example:
                    # region public

        :returns:
            Ture if any preprocesor is found.
        '''
        keywords = line.split(' ')
        if not '#' in line:
            return False
        elif has_any_keyword(line, preprocessors_to_search):
            return True
        else:
            keywords = line.split(' ')
            if len(keywords) == 1:
                # in this case the line is a preprocessor directive but
                # isnt the one I am looking for.
                return False

            if not '#' in keywords:
                # in this case the # is used as a value. For example:
                #   public string foo = '#';
                return False

            symbol_position = keywords.index('#')

            directives = map(lambda directive: directive.replace('#', ''), preprocessors_to_search)
            return keywords[symbol_position + 1] in directives


