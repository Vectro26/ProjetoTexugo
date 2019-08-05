# -*- coding: utf-8 -*-

'''
Tests for ``pywebuml.parsers.csharp.attribute_parser.CSharpAttributeParser``
'''

from unittest2 import TestCase
from pywebuml.models import Class
from pywebuml.parsers.csharp.attribute_parser import CSharpAttributeParser
from pywebuml.parsers.static_typed.package_manager import AbstractPackageManager


class PackageManagerMock(AbstractPackageManager):

    def get_class_package(self):
        return 'global'

    def get_package_for_type(self, type):
        return 'global.%s' % type



class CSharpAttributeParserTest(TestCase):

    def setUp(self):
        self.parser = CSharpAttributeParser()
        self.package_manager = PackageManagerMock('')
        self.class_model = Class('global', 'Foo', 'foo.cs', 'C#')


    def _parse(self, content, index):
        return self.parser.parse(self.class_model, content, index, self.package_manager)

    def test_parse_attribute_with_properties(self):
        ''' Test properties definitions. '''
        content = [
            "private int i { get { return foo; } }",
            "private int j { get { return foo; } set { foo = value; } };",
            "private int k {",
                    "get { return foo; }",
                    "set { foo = value }",
            "};",

            "private int l",
            "{",
                "get { return foo; }",
            "};",

            "public int m { get { return new Foo() } };",
            "public int n",
                "{  get { return new Foo() } };",

            "public int o",
                "{  set { _var = value } };",

            "public int p",
                "{  set { _var = value }, get { return new Foo() } };",

            "public int q { get ; set ; }",
            "public int r { get ; private set ; }",
        "}",
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(attr.name, 'i')

        index, attr = self._parse(content, 1)
        self.assertEquals(index, 2)
        self.assertEquals(attr.name, 'j')

        index, attr = self._parse(content, 2)
        self.assertEquals(index, 6)
        self.assertEquals(attr.name, 'k')

        index, attr = self._parse(content, 6)
        self.assertEquals(index, 10)
        self.assertEquals(attr.name, 'l')

        index, attr = self._parse(content, 10)
        self.assertEquals(index, 11)
        self.assertEquals(attr.name, 'm')

        index, attr = self._parse(content, 11)
        self.assertEquals(index, 13)
        self.assertEquals(attr.name, 'n')

        index, attr = self._parse(content, 13)
        self.assertEquals(index, 15)
        self.assertEquals(attr.name, 'o')

        index, attr = self._parse(content, 15)
        self.assertEquals(index, 17)
        self.assertEquals(attr.name, 'p')

        index, attr = self._parse(content, 17)
        self.assertEquals(index, 18)
        self.assertEquals(attr.name, 'q')

        index, attr = self._parse(content, 18)
        self.assertEquals(index, 19)
        self.assertEquals(attr.name, 'r')


    def test_ignoring_lanaguge_attributes(self):
        ''' Test that check if thi [index] is ignored. '''
        content = [
            "public int this [int index]",
            "{",
                "get",
                "{",
                    "return myArray[index];",
                "}",
                "set",
                "{",
                    "myArray[index] = value;",
                "}",
            "};",
        "}",
        ]
        index, attr = self._parse(content, 0)
        self.assertEquals(index, 11)
        self.assertTrue(attr is None)

