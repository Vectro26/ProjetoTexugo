# -*- coding: utf-8 -*-

'''
Test for ``pywebuml.parsers.static_typed.attribute_parser.AbstractStaticTypedAttributeParser
'''

from unittest2 import TestCase
from pywebuml.models import Class
from pywebuml.parsers.exceptions import (
                    ClossingArrayException,
                    EmptyNameException
                    )
from pywebuml.parsers.static_typed.attribute_parser import AbstractStaticTypedAttributeParser

class StaticTypedAttributeParser(AbstractStaticTypedAttributeParser):

    def get_referenced_class_complete_path(self, referenced_class_package, content):
        return 'mypackage.%s' % referenced_class_package



class PackageManagerMock(object):

    def get_package_for_type(self, variable_type):
        return 'mypackage.%s' % variable_type



class AbstractStaticTypedAttributeParserTest(TestCase):


    def setUp(self):
        self.parser = StaticTypedAttributeParser()
        self.class_model = Class('global', 'Foo', 'foo.cs', 'C#')
        self.package_manager = PackageManagerMock()


    def _parse(self, content, index):
        return self.parser.parse(self.class_model, content, index, self.package_manager)

    def test_parse_simple_attributes(self):
        ''' Test parsing some simple attributes. '''
        content = [
            "private int i;",
            "private int j = 3;",
            'private string k = "Helo World";',
            "private string l = null;",
            "string m;",
            'private bool? n;',
        "}" # this is for the end of the class definition
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(attr.name, 'i')
        self.assertEquals(attr.type, 'int')
        self.assertEquals(attr.referenced_class_package, None)

        index, attr = self._parse(content, 1)
        self.assertEquals(index, 2)
        self.assertEquals(attr.name, 'j')
        self.assertEquals(attr.type, 'int')
        self.assertEquals(attr.referenced_class_package, None)

        index, attr = self._parse(content, 2)
        self.assertEquals(index, 3)
        self.assertEquals(attr.name, 'k')
        self.assertEquals(attr.type, 'string')
        self.assertEquals(attr.referenced_class_package, None)

        index, attr = self._parse(content, 3)
        self.assertEquals(index, 4)
        self.assertEquals(attr.name, 'l')
        self.assertEquals(attr.type, 'string')
        self.assertEquals(attr.referenced_class_package, None)

        index, attr = self._parse(content, 4)
        self.assertEquals(index, 5)
        self.assertEquals(attr.name, 'm')
        self.assertEquals(attr.type, 'string')
        self.assertEquals(attr.referenced_class_package, None)

        index, attr = self._parse(content, 5)
        self.assertEquals(index, 6)
        self.assertEquals(attr.name, 'n')
        self.assertEquals(attr.type, 'bool?')
        self.assertEquals(attr.referenced_class_package, None)



    def test_parse_objects(self):
        ''' Test parsing some object values '''
        content = [
            "private Foo foo;",
            "private Bar bar = null;",
            "private FooBar other = new Foo();",
            "private IFoo another = new Foo(1, 2);",
        "}" # this is for the end of the class definition
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(attr.name, 'foo')
        self.assertEquals(attr.type, 'Foo')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Foo')

        index, attr = self._parse(content, 1)
        self.assertEquals(index, 2)
        self.assertEquals(attr.name, 'bar')
        self.assertEquals(attr.type, 'Bar')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Bar')

        index, attr = self._parse(content, 2)
        self.assertEquals(index, 3)
        self.assertEquals(attr.name, 'other')
        self.assertEquals(attr.type, 'FooBar')
        self.assertEquals(attr.referenced_class_package, 'mypackage.FooBar')

        index, attr = self._parse(content, 3)
        self.assertEquals(index, 4)
        self.assertEquals(attr.name, 'another')
        self.assertEquals(attr.type, 'IFoo')
        self.assertEquals(attr.referenced_class_package, 'mypackage.IFoo')


    def test_parse_arrays(self):
        ''' Test parsing attributes that are arrays. '''
        content = [
            "private int[] foo;",
            "private int[] i = new int[3];",
            "private int[] j = new int[2] { 1, 2};",
            "private int[] k = new int[2] {",
                "1, 2",
            "};",
            "private int[] l = new int[2] {",
                "1, 2 };",
            "private int[] m = new int[2]",
                "{",
                    "1",
                    "2",
                "};",

            "private int[] n = new int[2]",
                "{ 1,",
                "2 };",

        "}" # this is for the end of the class definition
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(attr.name, 'foo')
        self.assertEquals(attr.type, 'int[]')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 1)
        self.assertEquals(index, 2)
        self.assertEquals(attr.name, 'i')
        self.assertEquals(attr.type, 'int[]')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 2)
        self.assertEquals(index, 3)
        self.assertEquals(attr.name, 'j')
        self.assertEquals(attr.type, 'int[]')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 3)
        self.assertEquals(index, 6)
        self.assertEquals(attr.name, 'k')
        self.assertEquals(attr.type, 'int[]')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 6)
        self.assertEquals(index, 8)
        self.assertEquals(attr.name, 'l')
        self.assertEquals(attr.type, 'int[]')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 8)
        self.assertEquals(index, 13)
        self.assertEquals(attr.name, 'm')
        self.assertEquals(attr.type, 'int[]')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 13)
        self.assertEquals(index, 16)
        self.assertEquals(attr.name, 'n')
        self.assertEquals(attr.type, 'int[]')
        self.assertTrue(attr.referenced_class_package is None)


    def test_parse_attribute_with_spaces(self):
        ''' Test parsing and attribute that has more than 1 space between
        the words.'''
        content = [
            "private     int     i   =   3;",
            "private   Foo   j;",
        "}",
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(attr.name, 'i')
        self.assertEquals(attr.type, 'int')

        index, attr = self._parse(content, 1)
        self.assertEquals(index, 2)
        self.assertEquals(attr.name, 'j')
        self.assertEquals(attr.type, 'Foo')


    def test_final_static(self):
        ''' Test to get if a value is final and static. '''
        content = [
            "private int i = 0;",
            "private static string j;",
            "private const string k;",
            "private static readonly string m;",
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(attr.name, 'i')
        self.assertEquals(attr.is_final, False)
        self.assertEquals(attr.is_static, False)

        index, attr = self._parse(content, 1)
        self.assertEquals(index, 2)
        self.assertEquals(attr.name, 'j')
        self.assertEquals(attr.is_final, False)
        self.assertEquals(attr.is_static, True)

        index, attr = self._parse(content, 2)
        self.assertEquals(index, 3)
        self.assertEquals(attr.name, 'k')
        self.assertEquals(attr.is_final, True)
        self.assertEquals(attr.is_static, False)

        index, attr = self._parse(content, 3)
        self.assertEquals(index, 4)
        self.assertEquals(attr.name, 'm')
        self.assertEquals(attr.is_final, True)
        self.assertEquals(attr.is_static, True)


    def test_parsing_complex_structures(self):
        ''' Test parsing list, dictionaries, and arrays'''
        content = [
            "private List<Bar> i;",
            "private Dictionary<string, Val> j;",

            "private int [] k;",
            "private L L;",
            "private List <Foo> m;",
            "private List<List<Foo>> n;",
            "private List<string> o;",
            "private List<T> p;",
            "private Dictionary<string, List<Foo>> q;",
            "private Dictionary<Foo, List<string>> r;",
            "private Dictionary<Foo, List<Bar>> s;",
            "private Dictionary<string, List<bool>> t;",
            "private Dictionary<string, bool> u;",
            "private Dictionary<string, SortedDictionary<string, Foo>> v;",
        "}",
        ]

        index, attr = self._parse(content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(attr.name, 'i')
        self.assertEquals(attr.type, 'List<Bar>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Bar')

        index, attr = self._parse(content, 1)
        self.assertEquals(index, 2)
        self.assertEquals(attr.name, 'j')
        self.assertEquals(attr.type, 'Dictionary<string, Val>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Val')

        index, attr = self._parse(content, 2)
        self.assertEquals(index, 3)
        self.assertEquals(attr.name, 'k')
        self.assertEquals(attr.type, 'int []')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 3)
        self.assertEquals(index, 4)
        self.assertEquals(attr.name, 'L')
        self.assertEquals(attr.type, 'L')
        self.assertEquals(attr.referenced_class_package, 'mypackage.L')

        index, attr = self._parse(content, 4)
        self.assertEquals(index, 5)
        self.assertEquals(attr.name, 'm')
        self.assertEquals(attr.type, 'List <Foo>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Foo')

        index, attr = self._parse(content, 5)
        self.assertEquals(index, 6)
        self.assertEquals(attr.name, 'n')
        self.assertEquals(attr.type, 'List<List<Foo>>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Foo')

        index, attr = self._parse(content, 6)
        self.assertEquals(index, 7)
        self.assertEquals(attr.name, 'o')
        self.assertEquals(attr.type, 'List<string>')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 7)
        self.assertEquals(index, 8)
        self.assertEquals(attr.name, 'p')
        self.assertEquals(attr.type, 'List<T>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.T')

        index, attr = self._parse(content, 8)
        self.assertEquals(index, 9)
        self.assertEquals(attr.name, 'q')
        self.assertEquals(attr.type, 'Dictionary<string, List<Foo>>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Foo')

        index, attr = self._parse(content, 9)
        self.assertEquals(index, 10)
        self.assertEquals(attr.name, 'r')
        self.assertEquals(attr.type, 'Dictionary<Foo, List<string>>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Foo')

        index, attr = self._parse(content, 10)
        self.assertEquals(index, 11)
        self.assertEquals(attr.name, 's')
        self.assertEquals(attr.type, 'Dictionary<Foo, List<Bar>>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Foo')

        index, attr = self._parse(content, 11)
        self.assertEquals(index, 12)
        self.assertEquals(attr.name, 't')
        self.assertEquals(attr.type, 'Dictionary<string, List<bool>>')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 12)
        self.assertEquals(index, 13)
        self.assertEquals(attr.name, 'u')
        self.assertEquals(attr.type, 'Dictionary<string, bool>')
        self.assertTrue(attr.referenced_class_package is None)

        index, attr = self._parse(content, 13)
        self.assertEquals(index, 14)
        self.assertEquals(attr.name, 'v')
        self.assertEquals(attr.type, 'Dictionary<string, SortedDictionary<string, Foo>>')
        self.assertEquals(attr.referenced_class_package, 'mypackage.Foo')


    def test_parse_different_errors(self):
        ''' Test parsing different attributes when the file isn't correct.
        '''
        content = [
            "private int[] i = new int[2] {",
                "1,",
                "2",
        ]

        with self.assertRaises(ClossingArrayException) as cm:
            self._parse(content, 0)
            self.assertEquals(cm.expected.line, 0)


        content2 = [
            "THIS_MODIFIER_DOESNT_EXISTS int i = 2;",
            "moddifier1 moddifier2 int j = 3;",
            "private int;",
        ]

        with self.assertRaises(EmptyNameException) as cm:
            self._parse(content2, 0)
            self.assertEquals(cm.expected.line, 0)
            self.assertEquals(cm.name, 'int[] i')


        with self.assertRaises(EmptyNameException) as cm:
            self._parse(content2, 0)
            self.assertEquals(cm.expected.line, 0)
            self.assertEquals(cm.name, 'moddifier2 int[] i')


        with self.assertRaises(EmptyNameException) as cm:
            self._parse(content2, 1)
            self.assertEquals(cm.expected.line, 1)
            self.assertEquals(cm.name, '')


    def test_attribute_value_lines(self):
        ''' Test to take into account that the line of the attr could be in the next line.
        '''
        content = [
            "private int i;",
            "private int j = 3;",
            "private int k =",
                "4;",
            "private int l",
                "= 5;",
        "}"
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(attr.name, 'i');
        self.assertEquals(index, 1)

        index, attr =  self._parse(content, 1)
        self.assertEquals(attr.name, 'j');
        self.assertEquals(index, 2)

        index, attr =  self._parse(content, 2)
        self.assertEquals(attr.name, 'k');
        self.assertEquals(index, 4)

        index, attr =  self._parse(content, 4)
        self.assertEquals(attr.name, 'l');
        self.assertEquals(index, 6)







