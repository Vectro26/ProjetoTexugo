# -*- coding: utf-8 -*-

'''
Package manager implementation for c#.

@author: tzulberti
'''

from pywebuml.parsers.static_typed.package_manager import AbstractPackageManager
from pywebuml.parsers.utils import (
                has_any_keyword,
                remove_keywords
                )

class CSharpPackageManager(AbstractPackageManager):

    def __init__(self, content):
        super(CSharpPackageManager, self).__init__(content)
        self.indexes_and_namespaces = []
        self.parse_namespaces(content)

    def parse_namespaces(self, content):
        ''' Creates a list for each index, which namespace should be
        used. For example, if the list is
            [(0, 'global'), (3, 'unity'), (10, 'global')]

        for the class definitions between 0 and 2 the namespace that should
        be used is 'global', for the ones between 3 and 9 is **unity** and
        finally for all the ones between 10 and the end of the file is
        **global**.

        :parameters:
            content: list(str)
                the cleaned content of the file.
        '''
        if not has_any_keyword(content[0], ['namespace']):
            self.indexes_and_namespaces.append((0, 'global'))
        index = 0

        while True:
            if index >= len(content):
                break

            line = content[index]
            if has_any_keyword(line, ['namespace']):
                namespace = remove_keywords(line, ['namespace'])
                opened_blocks = 0
                if '{' in namespace:
                    opened_blocks = 1
                    # TODO missing test for the strip, and this case
                    namespace = namespace[: namespace.index('{')].strip()

                # go to the end of the namespace
                self.indexes_and_namespaces.append((index, namespace))
                while True:
                    index += 1
                    line = content[index]
                    opened_blocks += line.count('{') - line.count('}')
                    if opened_blocks == 0:
                        break

                if (index +1) < len(content) and not has_any_keyword(content[index+1], ['namespace']):
                    # if there are more lines in the file, and it doesn't
                    # defines a new namespace, then it has to
                    # restore the previous namespace
                    self.indexes_and_namespaces.append((index+1, 'global'))
            else:
                # this is the case of a previous namespace or
                # the global namespace.
                index += 1


    def get_class_package(self, index):
        ''' Return the name of the package based on the index.
        '''
        i = 0
        while i < len(self.indexes_and_namespaces) -1:
            if self.indexes_and_namespaces[i][0] <= index < self.indexes_and_namespaces[i+1][0]:
                return self.indexes_and_namespaces[i][1]
            i += 1

        return self.indexes_and_namespaces[-1][1]


    def get_package_for_type(self, variable_type):
        return 'global.%s' % variable_type





