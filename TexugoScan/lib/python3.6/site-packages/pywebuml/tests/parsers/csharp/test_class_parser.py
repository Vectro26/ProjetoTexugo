# -*- coding: utf-8 -*-

'''
Tests for pywebuml.initialize.parsers.csharp.class_parser:CSharpClassParser

This test will only focus in parsing the class singature. If you want to
see the whole parsing then check test_all_together.py. That module
has test for parsing attribute, class and methods together.
'''

from unittest2 import TestCase

from pywebuml.models import Class, Enum
from pywebuml.parsers.csharp.class_parser import CSharpClassParser




class CSharpClassParserTest(TestCase):

    # TODO: faltan  tests para:
    # cuando tira excepciones...

    def setUp(self):
        self.filepath = './tests/file.cs'
        self.attributes_parsed = 0
        self.methods_parsed = 0
        self.called_partial_class_mock = 0
        self.partial_class_mock = None
        self.parser = CSharpClassParser('content')
        self.parser.parse_attribute = self.mock_parse_attr
        self.parser.parse_method = self.mock_parse_method
        self.parser.find_partial_class = self.mock_find_partial_class

    def mock_parse_attr(self, content, index, current_class):
        self.attributes_parsed += 1
        return index +1

    def mock_parse_method(self, content, index, current_class):
        self.methods_parsed += 1
        return index +1

    def mock_find_partial_class(self, *args):
        ''' Mocked method for the find partial class of the parser.
        '''
        self.called_partial_class_mock += 1
        if self.called_partial_class_mock > 1:
            return self.partial_class_mock
        return None


    def test_parse_interface_and_inheritence(self):
        ''' Test what happens when the class extends or implements some
        interfaces.
        '''
        content = [
            "public class Foo : Bar",
            "{",
            "}",

            "public class Foo : Bar1,",
            "Bar2, Bar3",
            "{",
            "}",

            "public class Foo : Bar1,",
            "Bar2, Bar3 {",
            "}",


            "public class Foo : IBar",
            "{",
            "}",

            "public class Foo : IBar1, Bar1,",
            "Bar2, IBar2 {",
            "}",
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(index, 3)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo')
        self.assertEquals(len(klass.base_classes), 1)
        self.assertEquals(len(klass.implemented_interfaces), 0)
        self.assertEquals(klass.base_classes[0].base_class_package, 'global.Bar')


        index, klasses = self.parser.parse(self.filepath, content, 3)
        self.assertEquals(index, 7)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo')
        self.assertEquals(len(klass.base_classes), 3)
        self.assertEquals(len(klass.implemented_interfaces), 0)
        self.assertEquals(klass.base_classes[0].base_class_package, 'global.Bar1')
        self.assertEquals(klass.base_classes[1].base_class_package, 'global.Bar2')
        self.assertEquals(klass.base_classes[2].base_class_package, 'global.Bar3')


        index, klasses = self.parser.parse(self.filepath, content, 7)
        self.assertEquals(index, 10)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo')
        self.assertEquals(len(klass.base_classes), 3)
        self.assertEquals(len(klass.implemented_interfaces), 0)
        self.assertEquals(klass.base_classes[0].base_class_package, 'global.Bar1')
        self.assertEquals(klass.base_classes[1].base_class_package, 'global.Bar2')
        self.assertEquals(klass.base_classes[2].base_class_package, 'global.Bar3')

        index, klasses = self.parser.parse(self.filepath, content, 10)
        self.assertEquals(index, 13)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo')
        self.assertEquals(len(klass.base_classes), 0)
        self.assertEquals(len(klass.implemented_interfaces), 1)
        self.assertEquals(klass.implemented_interfaces[0].interface_class_package, 'global.IBar')


        index, klasses = self.parser.parse(self.filepath, content, 13)
        self.assertEquals(index, 16)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo')
        self.assertEquals(len(klass.base_classes), 2)
        self.assertEquals(len(klass.implemented_interfaces), 2)
        self.assertEquals(klass.implemented_interfaces[0].interface_class_package, 'global.IBar1')
        self.assertEquals(klass.implemented_interfaces[1].interface_class_package, 'global.IBar2')
        self.assertEquals(klass.base_classes[0].base_class_package, 'global.Bar1')
        self.assertEquals(klass.base_classes[1].base_class_package, 'global.Bar2')



    def test_operator_is_method(self):
        current_class = Class('global.Foo', 'Foo', 'foo.cs', 'C#')
        current_line = "public static bool operator !=(Foo lhs, Foo rhs)"
        is_method = self.parser.is_method(current_line, current_class)
        self.assertTrue(is_method)


    def test_oneline_inner_with_extends_classes(self):
        ''' Test parsing inner classes when they extend another class. '''
        content = [
            'public class Foo : Base',
            '{',
                'public new class Inner1 : Base.Inner1 {}',
                'public new class Inner2: Base.Inner2 {}',
            '}',
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(index, 5)
        self.assertEquals(len(klasses), 3)
        self.assertEquals(klasses[0].package, 'global.Foo')
        self.assertEquals(klasses[0].base_classes[0].base_class_package, 'global.Base')
        self.assertEquals(len(klasses[0].inner_classes), 2)
        self.assertEquals(klasses[1].package, 'global.Foo.Inner1')
        self.assertEquals(klasses[1].base_classes[0].base_class_package, 'global.Base.Inner1')
        self.assertEquals(klasses[2].package, 'global.Foo.Inner2')
        self.assertEquals(klasses[2].base_classes[0].base_class_package, 'global.Base.Inner2')


    def test_partial_classes(self):
        ''' Test parsing some partial classes, '''
        content = [
            "public partial class Foo",
            "{",
                "private int i",
                "public Foo() {}",
            "}",

            "public partial class Foo",
            "{",
                "private int j",
                "public Foo(int k) {}",
            "}",
        ]


        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(len(klasses), 1)
        self.assertEquals(self.called_partial_class_mock, 1)
        self.assertEquals(self.methods_parsed, 1)
        self.assertEquals(self.attributes_parsed, 1)

        self.partial_class_mock =   klasses[0]

        index, klasses = self.parser.parse(self.filepath, content, 5)
        self.assertEquals(len(klasses), 1)
        self.assertTrue(klasses[0] is self.partial_class_mock)
        self.assertEquals(self.called_partial_class_mock, 2)
        self.assertEquals(self.methods_parsed, 2)
        self.assertEquals(self.attributes_parsed, 2)


    def test_parse_enum_inheritance(self):
        ''' Test what happens when an enum extends a class. '''
        content = [
            "public enum Foo : Bar, IFoo {",
                 "FIRST,",
                "SECOND,",
                "LAST;",

                "public Foo(int k) { }",

            "}",
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(len(klasses), 1)
        self.assertTrue(isinstance(klasses[0], Enum))
        self.assertEquals(self.attributes_parsed, 3)
        self.assertEquals(self.methods_parsed, 1)
        self.assertEquals(len(klasses[0].base_classes), 1)
        self.assertEquals(len(klasses[0].implemented_interfaces), 1)
