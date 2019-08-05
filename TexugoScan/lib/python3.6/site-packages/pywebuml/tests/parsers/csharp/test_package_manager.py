# -*- coding: utf-8 -*-

'''
Has some tests for `pywebuml.parsers.csharp.package_manager.CSharpPackageManager`
'''

from unittest2 import TestCase
from pywebuml.parsers.csharp.package_manager import CSharpPackageManager

class TestCSharpPackageManager(TestCase):

    def test_parse_file_with_no_namespace(self):
        ''' Test parsing the content of a file that doesn't has a namespace.
        '''
        content = [
            'public class Foo',
            '{',
                'int Bar;',
            '}',
        ]
        manager = CSharpPackageManager(content)
        self.assertEquals(manager.indexes_and_namespaces,
                            [(0, 'global')])


    def test_parse_contet_namespace_definition(self):
        ''' Test parsing a file that has a namespace definition.
        '''
        content = [
            'namespace Bar',
            '{',
                'public class Foo',
                '{',
                '}',
            '}',
        ]
        manager = CSharpPackageManager(content)
        self.assertEquals(manager.indexes_and_namespaces,
                            [(0, 'Bar')])


    def test_parse_content_not_starting_namespace(self):
        ''' Test parsing the content when the file doesn't start with a namespace
        definition.
        '''
        content = [
            'using System;',
            'namespace Bar',
            '{',
                'public class Foo',
                '{',
                '}',
            '}',
        ]
        manager = CSharpPackageManager(content)
        self.assertEquals(manager.indexes_and_namespaces,
                            [(0, 'global'), (1, 'Bar')])


    def test_parse_content_with_clases_outside_namespaces(self):
        ''' Test parsing the content when the file doesn't start with a namespace
        definition.
        '''
        content = [
            'using System;',
            'namespace Bar',
            '{',
                'public class Foo',
                '{',
                '}',
            '}',

            'public class FooBar',
            '{',
            '}',
        ]
        manager = CSharpPackageManager(content)
        self.assertEquals(manager.indexes_and_namespaces,
                            [(0, 'global'), (1, 'Bar'), (7, 'global')])


    def test_parsing_two_namespaces(self):
        ''' Test parsing the content when it has 2 namespaces.
        '''
        content = [
            'using System;',
            'namespace Bar',
            '{',
                'public class Foo',
                '{',
                '}',
            '}',

            'namespace Bar2',
            '{',
                'public class FooBar',
                '{',
                '}',
            '}',
        ]
        manager = CSharpPackageManager(content)
        self.assertEquals(manager.indexes_and_namespaces,
                            [(0, 'global'), (1, 'Bar'), (7, 'Bar2')])


    def test_parsing_two_namepsace_and_lines_between(self):
        ''' Test parsing two namespaces that have some code between them.
        '''
        content = [
            'using System;',
            'namespace Bar',
            '{',
                'public class Foo',
                '{',
                '}',
            '}',

            'public class Foo2',
            '{',
            '}',

            'namespace Bar2',
            '{',
                'public class Foo3',
                '{',
                '}',
            '}',
        ]
        manager = CSharpPackageManager(content)
        self.assertEquals(manager.indexes_and_namespaces,
                            [(0, 'global'), (1, 'Bar'), (7, 'global'), (10, 'Bar2')])


    def test_getting_namespace_of_class_definition(self):
        ''' Test getting the namespace for a defined class.
        '''
        content = [
            'using System;',
            'namespace Bar',
            '{',
                'public class Foo',
                '{',
                '}',
            '}',

            'public class Foo2',
            '{',
            '}',

            'namespace Bar2',
            '{',
                'public class Foo3',
                '{',
                '}',
            '}',

            'public class Foo4',
            '{',
            '}',
        ]

        manager = CSharpPackageManager(content)
        self.assertEquals(manager.get_class_package(3), 'Bar')
        self.assertEquals(manager.get_class_package(7), 'global')
        self.assertEquals(manager.get_class_package(12), 'Bar2')
        self.assertEquals(manager.get_class_package(16), 'global')




