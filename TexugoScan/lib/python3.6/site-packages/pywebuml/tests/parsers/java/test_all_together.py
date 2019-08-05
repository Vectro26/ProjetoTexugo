# -*- coding: utf-8 -*-

'''
Has some basic tests for the Java parser.
'''

from unittest2 import TestCase
from pywebuml.parsers.java.file_parser import JavaFileParser

class JavaAllTogetherTest(TestCase):

    def setUp(self):
        self.filepath = './foo.java'
        self.parser = JavaFileParser()


    def test_parse_empty_class(self):
        ''' Test parsing a simple class.
        '''
        content = [
            'public class Foo',
            '{',
            '}',
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0].name, 'Foo')


    def test_parse_simple_class(self):
        ''' Test parsing a class that has attributes and methods.
        '''
        content = [
            'public class Foo',
            '{',
                'private int i = 0;',
                'public String toString()',
                '{',
                    'return "Foo";',
                '}',
            '}',
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 1)
        self.assertEquals(len(res[0].attributes), 1)
        self.assertEquals(len(res[0].methods), 0)


    def test_parse_class_with_external_references(self):
        ''' Test parsing a class that references an external class.
        '''
        content = [
            'package myprogram.mypackage;',
            'import myprogram.interfaces.IFoo;',

            'public class Foo implements IFoo extends Base',
            '{',

                'public int i = 0;',
                'public Another j = null;',
            '}'
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 1)
        self.assertEquals(len(res[0].attributes), 2)
        self.assertEquals(res[0].attributes[1].referenced_class_package, 'myprogram.mypackage.Another')
        self.assertEquals(len(res[0].methods), 0)


    def test_parse_enum_file(self):
        ''' Test parsing a class where the only data is an enum.
        '''
        content = [
            'package mypackage;',

            'public enum Foo',
            '{',
                'FIRST,',
                'lAST',
            '}',
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 1)

