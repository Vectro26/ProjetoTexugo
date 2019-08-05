# -*- coding: utf-8 -*-

'''
Has some basic tests for `pywebuml.parsers.java.file_parser:JavaFileParser`
'''

from unittest2 import TestCase

from pywebuml.parsers.java.file_parser import JavaFileParser

class TestJavaFileParser(TestCase):

    def setUp(self):
        self.parser = JavaFileParser()


    def test_remove_annotations(self):
        ''' Test removin simple class or method annotations.
        '''
        content = [
            '@ContextConfiguration(locations = {',
                        '"classpath: **/mycontext-test.xml",',
		                '"classpath: **/applicationTestContext.xml" },',
		                'loader = GenericXmlContextLoader.class)',
            'public class Foo',
            '{',
                '@Autowired',
                'public Bar bar',

                '@Override',
                'public String toString()',
                '{',
                    'return "Foo"',
                '}',

                '@SuppressWarnings("unchequed")',
                'public List<Bar> getList()',
                '{',
                    'return None',
                '}',

            '}',
        ]
        expected = [
            'public class Foo',
            '{',
                'public Bar bar',

                'public String toString()',
                '{',
                    'return "Foo"',
                '}',

                'public List<Bar> getList()',
                '{',
                    'return None',
                '}',

            '}',
        ]
        actual = self.parser.clean_content(content)
        self.assertEquals(actual, expected)



    def test_remove_inline_annotations(self):
        ''' Test removing inline decorators.
        '''
        content = [
            'public @interface Foo',
            '{',
                '@Override public method Foo()',
            '}',
        ]
        expected = [
            'public  Foo',
            '{',
                ' public method Foo()',
            '}',
        ]
        actual = self.parser.clean_content(content)
        self.assertEquals(actual, expected)


    def test_remove_static_code(self):
        ''' Test removing static code.
        '''
        content = [
            'public class Foo',
            '{',
                'public static final int MAX = 5;',

                'static {',
                    'some Logic here...',
                '}',

                'public static fina int MIN = 0;'
            '}',
        ]
        expected = [
            'public class Foo',
            '{',
                'public static final int MAX = 5;',

                'public static fina int MIN = 0;'
            '}',
        ]
        actual = self.parser.clean_content(content)
        self.assertEquals(actual, expected)


    def test_remove_static_code_another_line(self):
        ''' Test removing static code that is defined in the following line.
        '''
        content = [
            'public class Foo',
            '{',
                'public static final int MAX = 5;',

                'static',
                '{',
                    'some Logic here...',
                '}',

                'public static fina int MIN = 0;'
            '}',
        ]
        expected = [
            'public class Foo',
            '{',
                'public static final int MAX = 5;',

                'public static fina int MIN = 0;'
            '}',
        ]
        actual = self.parser.clean_content(content)
        self.assertEquals(actual, expected)


    def test_remove_annotations_and_static(self):
        ''' Test removing annotations and static code.
        '''
        content = [
            'public class Foo',
            '{',
                'public static final int MAX = 5;',

                'static',
                '{',
                    'some Logic here...',
                '}',

                'public static fina int MIN = 0;'

                '@Override public String toString() {',
                    'return "Foo";',
                '}',
            '}',
        ]
        expected = [
            'public class Foo',
            '{',
                'public static final int MAX = 5;',
                'public static fina int MIN = 0;'
                ' public String toString() {',
                    'return "Foo";',
                '}',
            '}',
        ]
        actual = self.parser.clean_content(content)
        self.assertEquals(actual, expected)


    def test_should_ignore_line(self):
        ''' Test if the code line should be ignored or not.
        '''
        ignore_lines = [
            'package myproject.mypackage.Foo;',
            'import apache.utils.Bar;',
            'import apache.*;'
        ]
        for line in ignore_lines:
            self.assertTrue(self.parser.should_ignore_line(line, []))

        not_ignore_lines = [
            'int mypackage = 3;',
            'int maximports = 4;'
        ]
        for line in not_ignore_lines:
            self.assertFalse(self.parser.should_ignore_line(line, []))


