# -*- coding: utf-8 -*-

'''
Tests for pywebuml.parsers.static_typed.class_parser:AbstractStaticTypedClassParser
'''

from unittest2 import TestCase

from pywebuml.models import Class, Enum, Interface, Abstract
from pywebuml.parsers.static_typed.class_parser import AbstractStaticTypedClassParser



class PackageManagerMock(object):

    def get_class_package(self, index):
        return 'global'


class MethodParserMock(object):

    def parse(self, current_class, content, index):
        return (index + 1, [])


class AttributeParserMock(object):

    def parse(self, current_class, content, index, package_manager):
        return (index + 1, [])


class StaticTypedClassParerMock(AbstractStaticTypedClassParser):

    def __init__(self):
        super(StaticTypedClassParerMock, self).__init__('')
        self.attributes_parsed = 0
        self.methods_parsed = 0


    def get_programming_language(self):
        return 'MyLanguage'

    def is_other_type(self, current_line):
        return False

    def get_attribute_parser(self):
        self.attributes_parsed += 1
        return AttributeParserMock()

    def get_method_parser(self):
        self.methods_parsed += 1
        return MethodParserMock()

    def get_class_definition_data(self, class_definition, content):
        return class_definition.strip(), [], []

    def get_package_manager(self, content):
        return PackageManagerMock()


class AbstractStaticTypedClassParser(TestCase):

    # TODO: faltan  tests para:
    # cuando tira excepciones...

    def setUp(self):
        self.filepath = './tests/file.cs'
        self.called_partial_class_mock = 0
        self.partial_class_mock = None
        self.parser = StaticTypedClassParerMock()


    def test_parsing_different_classes(self):
        ''' Test parsing opening and closing { and } positions. '''
        content = [
            "public class Foo1 { };",

            "public class Foo2 {",
            "}",

            "public class Foo3",
            "{",
            "}",
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(index, 1)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo1')

        index, klasses = self.parser.parse(self.filepath, content, 1)
        self.assertEquals(index, 3)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo2')

        index, klasses = self.parser.parse(self.filepath, content, 3)
        self.assertEquals(index, 6)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.name, 'Foo3')


    def test_check_if_method_or_attribute(self):
        ''' Test to check if a line is a method or attribute. '''
        content = [
            "private int i;",
            "private int i = 3;",
            "private Foo i = new Foo();",
            "private Foo i;",
            "private int bar",
            "private int bar {",
            "public int bar { get { return value; }, set { _bar = value; } };",
            "public int bar { get  { return mVar; } }",
            "public int bar { set { _bar = value: } }",
            "int[] bar",
            "int[] bar = new int[2] { 1, 2}",
            "int[] bar = new int[2] {",
            "Foo[] bar = new Foo[1] { new Foo(1, 2) }",
            "public Foo()",
            "public void Foo() {",
            "public void Foo()",
            "public void Foo() { foo = 2};",
            "public void Foo() { return 3 };",
            "public void Foo(int bar)",
            "public void Foo(int bar) {",
            "public void Foo(int bar) { foo = 3 };",
            "public int getValue()",
            "public int setValue()",
            "private Dictionary<string, T?> method1() where T : new",
        ]
        current_class = Class('global.Foo', 'Foo', 'foo.cs', 'C#')
        for index, current_line in enumerate(content):
            is_method = index >= 13
            self.assertEquals(self.parser.is_method(current_line, current_class), is_method, msg=current_line)


    def test_parse_inner_class(self):
        ''' Test parsing some inner classes. '''
        content = [
            "public class Foo",
            "{",
                "private class Inner1 {}",
                "private class Inner2 {",
                "}",
                "private class Inner3",
                "{",
                "}",

                "public struct Inner4",
                "{",
                "}",
            "}",
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(index, 12)
        self.assertEquals(len(klasses), 5)
        self.assertEquals(klasses[0].package, 'global.Foo')
        self.assertEquals(len(klasses[0].inner_classes), 4)

        for index, klass in enumerate(klasses[1:]):
            self.assertEquals(klass.package, 'global.Foo.Inner%s' % (index +1))
            self.assertEquals(klass.owner, klasses[0])

        self.assertEquals(klasses[0].inner_classes, klasses[1:])


    def test_parse_interface(self):
        ''' Test parsing an interface. '''
        content = [
            "public interface Foo1",
            "{",
            "}",

            "public abstract Foo2",
            "{",
            "}",

            "public class Foo3",
            "{",
            "}",
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.package, 'global.Foo1')
        self.assertTrue(isinstance(klass, Interface))

        index, klasses = self.parser.parse(self.filepath, content, 3)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.package, 'global.Foo2')
        self.assertTrue(isinstance(klass, Abstract))

        index, klasses = self.parser.parse(self.filepath, content, 6)
        self.assertEquals(len(klasses), 1)
        klass = klasses[0]
        self.assertEquals(klass.package, 'global.Foo3')
        self.assertFalse(isinstance(klass, (Abstract, Interface)))


    def test_parse_class_with_attr_and_methods(self):
        ''' Test a whole class but with some mocked methods. '''
        content = [
            "public class Foo",
            "{",
                "private int i;",

                "public Foo() : base() { this.i = 1 }",
                "private int  l = 2;",
            "}",
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(len(klasses), 1)
        self.assertEquals(self.parser.methods_parsed, 1)
        self.assertEquals(self.parser.attributes_parsed, 2)


    def test_parse_enums(self):
        ''' Test parsing some enums. '''
        content = [
            "public enum Foo {",
                "FIRST,",
                "SECOND,",
                "LAST;",

                "public Foo(int k) { }",
            "}",
        ]

        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(len(klasses), 1)
        self.assertTrue(isinstance(klasses[0], Enum))
        self.assertEquals(self.parser.attributes_parsed, 3)
        self.assertEquals(self.parser.methods_parsed, 1)


    def test_parse_enums_with_constructors(self):
        ''' Test parse enums whose attributes have constructors. '''
        content = [
            "public enum Foo {",
                "FIRST (1),",
                "SECOND (2),",
                "LAST (3);",

                "public Foo(int k) {}",
                "public int getValue() { }",
            "}",
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(len(klasses), 1)
        self.assertTrue(isinstance(klasses[0], Enum))
        self.assertEquals(self.parser.attributes_parsed, 3)
        self.assertEquals(self.parser.methods_parsed, 2)


    def test_parse_enum_as_inner(self):
        ''' Test what happens when the enum is defined inside another class.
        '''
        content = [
            'public Foo',
            '{',
                'public enum Bar',
                '{',
                    'FIRST;',
                '}',

                'public class Another',
                '{',
                '}',
            '}',
        ]
        index, klasses = self.parser.parse(self.filepath, content, 0)
        self.assertEquals(len(klasses), 3)
        self.assertEquals(klasses[0].name, 'Foo')
        self.assertTrue(isinstance(klasses[0], Class))
        self.assertEquals(klasses[1].name, 'Bar')
        self.assertTrue(isinstance(klasses[1], Enum))
        self.assertEquals(klasses[2].name, 'Another')
        self.assertEquals(klasses[2].owner, klasses[0])
        self.assertEquals(klasses[0].inner_classes,
                            [klasses[1], klasses[2]])

