# -*- coding: utf-8 -*-

'''
Tests for pywebuml.initialize.parsers.csharp.file_parser:CSharpFileParser

As with the class parser test, this test won't have tests for parsing a whole
file. This class will only test the generic file parsing and won't test the
parsing of a class.
'''

from unittest2 import TestCase
from pywebuml.parsers.csharp.file_parser import CSharpFileParser

class CSharpFileParserTest(TestCase):
    ''' Some basic tests for the file parsing.
    '''

    def mock_class_parsing(self, filepath, content, index, res):
        ''' Mock so that it doesn't parse a class. '''
        self.classes_found += 1
        return index + 1


    def setUp(self):
        self.classes_found = 0
        self.filepath = './test/foo.cs'
        self.parser = CSharpFileParser()
        self.parser.parse_class_definition = self.mock_class_parsing


    def test_parse_simple_file(self):
        ''' Test parsing a simple file. '''
        content = [
            "public class Foo { }"
        ]
        self.parser.parse_content(self.filepath, content)
        self.assertEquals(self.classes_found, 1)


    def test_parse_with_namespace(self):
        ''' Test parsing a file that has a namespace. '''
        content = [
            "public class Bar {}",
            "namespace foo1 {",
               "public class Bar {}",
            "}",

            "namespace foo2",
            "{",
                "public class Bar {}",
            "}",

            "public class Bar {}",
        ]
        self.parser.parse_content(self.filepath, content)
        self.assertEquals(self.classes_found, 4)



    def test_has_preprocessor_value(self):
        ''' Some tests to the have preprocessor value method.
        '''
        actual = self.parser._has_preprocessor_value('using System;', ['#if'])
        self.assertEquals(actual, False)

        actual = self.parser._has_preprocessor_value('#if DEFINED_VAR', ['#if'])
        self.assertEquals(actual, True)

        actual = self.parser._has_preprocessor_value('#if DEFINED_VAR', ['#else'])
        self.assertEquals(actual, False)

        actual = self.parser._has_preprocessor_value('private string foo = "#";', ['#else'])
        self.assertEquals(actual, False)


    def test_parse_simple_precompiler_directive(self):
        ''' Test what happens when the file has a simple compiler directive.
        '''
        content = [
            "#define FOO",
            "#if FOO",
                "public class Bar {}",
            "#endif",
        ]
        expected = [
            "public class Bar {}",
        ]
        actual = self.parser.remove_preprocessor_code(content)
        self.assertEquals(actual, expected)


    def test_parse_if_else_precompiler_directives(self):
        ''' Checks what happens when the file has an #if, #else and #endif.
        '''
        content = [
            "#define FOO",
            "#if FOO",
                "public class Bar {",
            "#else",
                "public class Foo {",
            "#endif",

            "}",
        ]
        expected = [
            'public class Bar {',
            '}'
        ]
        actual = self.parser.remove_preprocessor_code(content)
        self.assertEquals(actual, expected)


    def test_complicated_preprocessor_ifs(self):
        ''' Test what happens if there are some #if, #elif, #else
        '''
        content = [
            '#define FOO',
            '#define BAR',
            '#if PEPE',
                'public class Bar1 {}',
            '#elif PEPE2',
                'public class Bar2 {}',
            '#else',
                'public class Bar3 {}',
            '#endif',
        ]
        expected = [
            'public class Bar3 {}',
        ]
        actual = self.parser.remove_preprocessor_code(content)
        self.assertEquals(actual, expected)


    def test_nested_ifs(self):
        ''' Test what happens with nested ifs.
        '''
        content = [
            '#define FOO',
            '#define BAR',

            '#if PEPE',
                '#if FOO',
                    'LINE 1',
                '#endif',
                'LINE 2',

            '#else',
                '#if FOO',
                    '#undef BAR',
                    '#if BAR',
                        'LINE 3',
                    '#endif',
                    'LINE 4',
                '#endif',
            '#endif',
        ]
        expected = [
            'LINE 4',
        ]
        actual = self.parser.remove_preprocessor_code(content)
        self.assertEquals(actual, expected)


    def test_other_preprocessors_directives(self):
        ''' Test that it also removes the other preprocessor directives.
        '''
        content = [
            '#define FOO',
            '#if FOO',
                '#warning DEBUG is defined',
                '#region BAR',
                    'public class Bar {}',
                '#endregion',
            '#endif',

            '#error This is an error',
        ]
        expected = [
            'public class Bar {}',
        ]
        actual = self.parser.remove_preprocessor_code(content)
        self.assertEquals(actual, expected)


    def test_remove_all_preprocessor_directives_with_spaces(self):
        ''' Test removing all preprocessor directives when there is not if.
        '''
        content = [
            'using System;',
            'public class Foo',
            '{',
                '# region publics',
                'public int foo;',
                '# endregion',
            '}',
        ]
        expected = [
            'using System;',
            'public class Foo',
            '{',
                'public int foo;',
            '}',
        ]
        actual = self.parser.remove_preprocessor_code(content)
        self.assertEquals(actual, expected)



    def test_remove_decorators(self):
        ''' Test removing C# decorators.
        '''
        content = [
            '[TestClass]',
            'public MyUnittest {',

                '[TestMethod}',
                'public void testMethod() {}',
            '}',
        ]
        expected = [
            'public MyUnittest {',
                'public void testMethod() {}',
            '}',
        ]
        actual = self.parser.clean_content(content)
        self.assertEquals(actual, expected)
