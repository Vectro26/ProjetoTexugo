# -*- coding: utf-8 -*-

'''
Created on 13/03/2011
@author: tzulberti
'''

from pywebuml.parsers.static_typed.file_parser import AbstractStaticTypedFileParser
from pywebuml.parsers.java.class_parser import JavaClassParser
from pywebuml.parsers.utils import has_any_keyword

class JavaFileParser(AbstractStaticTypedFileParser):
    ''' Parser for java files.
    '''

    def get_class_parser(self, content):
        return JavaClassParser(content)


    def should_ignore_line(self, current_line, content):
        ''' Ignore the lines that are the package or import classes.
        '''
        if has_any_keyword(current_line, ['package', 'import']):
            self.index += 1
            return True

        return False


    def clean_content(self, content):
        ''' Remove all the annotations and static code of the file.
        '''
        res = []
        index = 0
        while True:
            line = content[index]
            if '@' in line:
                # in this case, the annotation in somewhere in the line.
                # For example:
                #   public @interface Documentation {
                #   }
                # or
                #   @Override public void foo() {
                #   }
                start = line.index('@')
                end = start
                opened_parenthesis = line.count('(') - line.count(')')
                while opened_parenthesis != 0:
                    # then the annotation uses more then one line
                    index += 1
                    line += content[index]
                    opened_parenthesis = line.count('(') - line.count(')')

                opened_parenthesis = 0
                while True:
                    end += 1
                    current_char = line[end]
                    if current_char == ' ' and opened_parenthesis == 0:
                        break
                    elif current_char == '(':
                        opened_parenthesis += 1
                    elif current_char == ')':
                        opened_parenthesis -= 1

                    if end == len(line) - 1:
                        # in this case the line ends with the decorator.
                        # For example:
                        #   // ! @Transient(readOnly = false)
                        end += 1
                        break

                line = line[:start] + line[end:]

                if line:
                    # take into account that the value of the line
                    # could only be a decorator. For example:
                    #       @Override
                    #       public void foo() {
                    res.append(line)
            elif line == 'static {' or line == 'static':
                # remove the static blocks of the file.
                # because this aren't methors or attributes.
                position = index
                if not '{' in line:
                    position += 1

                opened_keys = 0
                while True:
                    tmp = content[position]
                    opened_keys = opened_keys + tmp.count('{') - tmp.count('}')
                    position += 1
                    if opened_keys == 0:
                        break
                index = position -1

            else:
                res.append(line)

            index += 1
            if index == len(content):
                break

        return res





