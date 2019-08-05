# -*- coding: utf-8 -*-

'''
Some tests for the
`pywebuml.parsers.static_typed.file_parser.AbstractStaticTypedFileParser`
'''

from unittest2 import TestCase
from pywebuml.parsers.static_typed.file_parser import AbstractStaticTypedFileParser


class StaticTypedClassParserMock(object):
    ''' Mocks the class parsers.
    '''

    def __init__(self):
        self.called_indexes = []

    def parse(self, filepath, content, index, owner = None):
        self.called_indexes.append(index)
        return (index +1, [])


class StaticTypedFileParserMock(AbstractStaticTypedFileParser):
    ''' Mock class to override the abstract methods.
    '''

    def __init__(self):
        self.clean_content_called = 0
        self.get_current_namespace_called = 0
        self.should_ignore_line_called = 0
        self.get_class_parser_called = 0

        super(StaticTypedFileParserMock, self).__init__()


    def clean_content(self, content):
        self.clean_content_called += 1
        return content


    def get_current_namespace(self, *args):
        self.get_current_namespace_called += 1
        return 'foo'


    def should_ignore_line(self, *args):
        self.should_ignore_line_called += 1
        return False


    def get_class_parser(self, content):
        self.get_class_parser_called += 1
        return StaticTypedClassParserMock()


class StaticTypedFileParserTest(TestCase):

    def setUp(self):
        self.parser = StaticTypedFileParserMock()


    def test_parse_empyt_file(self):
        ''' Test parsing an empty file.
        '''
        content = []
        res = self.parser.parse_content('./foo.cs', content)
        self.assertEquals(res, [])

    def test_remove_comments(self):
        ''' Test that the utils method to remove comments is used.
        '''
        content = [
            '// this is a comment',
            'public class Foo {}',
        ]
        self.parser.parse_content('./foo.cs', content)
        self.assertEquals(self.parser.class_parser.called_indexes, [0])


    def test_parse_commented_file(self):
        ''' Test parsing a file that is a whole comment.
        '''
        content = [
            '/*',
            'public class Foo {}',
            '*/',
        ]
        res = self.parser.parse_content('./foo.cs', content)
        self.assertEquals(res, [])


    def test_uses_clean_content(self):
        ''' Test to check that the remove content is used.
        '''
        content = [
            'public class Foo {}',
        ]
        self.parser.parse_content('./foo.cs', content)
        self.assertEquals(self.parser.clean_content_called, 1)


    def test_uses_should_ignore_line(self):
        ''' Test to check that the should_ignore_line is used.
        '''
        content = [
            'public class Foo {}',
        ]
        self.parser.parse_content('./foo.cs', content)
        self.assertEquals(self.parser.should_ignore_line_called, 1)


    def test_ingore_methods_before_class(self):
        ''' Test that it will ignore the methods and attributes before
        the class definition.
        '''
        content = [
            'int i = 3;',
            'public string foo() {',
                'return "this is a method"',
            '}',
            'public class Foo {}',
        ]
        self.parser.parse_content('./foo.cs', content)
        self.assertEquals(self.parser.class_parser.called_indexes, [4])

        # TODO agregar los tests que faltan
