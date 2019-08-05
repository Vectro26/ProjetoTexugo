# -*- coding: utf-8 -*-

'''
Test that parse class and it's attributes and methods.

In this test nothing will be mocked.
'''

from unittest2 import TestCase
from pywebuml.models import Enum
from pywebuml.parsers.csharp.file_parser import CSharpFileParser
from pywebuml.parsers.exceptions import (
                    EmptyNameException
                    )

class CSharpAllTogetherTest(TestCase):

    # TODO: falta
    # - test que le pegue a la base de datos
    # - ver los casos de excepciones...
    # - agregar test donde el comentario este pegado a la palabra: //just because...

    # testear casos en donde tenga documentacion como esta. Ver if 72 del base
    # ///*********************
    # /// Esto es el comentario
    # ///*********************



    def setUp(self):
        self.filepath = './test'
        self.parser = CSharpFileParser()

    def test_simple_class_definition(self):
        ''' Test some simple class definitions. '''
        content = [
            "using System",
            "namespace foo"
            "{",
                "public class Bar : IBar, SuperMyClass",
                "{",
                    "private int i = 3;",

                    "public Bar(int i, int j)",
                        ": base(i, j)",
                    "{",
                        "this.i = i * j;",
                    "}",

                    "protected void foo()",
                    "{",
                        "doSomething();",
                    "}",

                "}",
            "}",
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 1)
        klass = res[0]
        self.assertEquals(klass.package, 'foo.Bar')
        self.assertEquals(len(klass.attributes), 1)
        self.assertEquals(klass.attributes[0].name, 'i')
        self.assertEquals(len(klass.methods), 2)
        self.assertEquals(klass.methods[0].signature, 'Bar(int i, int j)')
        self.assertEquals(klass.methods[1].signature, 'void foo()')

    def test_parse_documented_class(self):
        ''' Checks what happens when the class is documented. '''
        content = [
            'public class Foo',
            '{',
                'private int i = 3; // this is a value of the class',

                "/* private int j this shouldn't be taken into account */",

                '/* this method is documented',
                '* public void bar()',
                '* {',
                    '* return ;',
                '* }',
                '*/',

                'private int k = 4;',

            '}',
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 1)
        klass = res[0]
        self.assertEquals(klass.package, 'global.Foo')
        self.assertEquals(len(klass.methods), 0)
        self.assertEquals(len(klass.inner_classes), 0)
        self.assertEquals(len(klass.attributes), 2)


    def test_complicated_together(self):
        ''' Test all together in a more complicated case. '''
        content = [
            "using System",
            "namespace Foo1 {",
                "public class Bar1 {",
                    "public struct Inner1",
                    "{",
                        "private int i;",

                        "public void inner1()",
                        "{",
                            "doSomething();",
                        "}",
                    "}",

                    "public class Inner2 : IInner2 { }",

                    "private Inner1 instance;",
                    "private int i;",

                    "public void foo()",
                    "{",
                        "doSomething();",
                    "}",
                "}",
            "}",

            "namespace Foo2",
            "{",
                "/**",
                "* This whole class is documented.",
                "* public class Bar2 {",
                    "* private int i = 3;",
                    "* public void foo() {",
                        "* doSomething();",
                    "* }",
                "* }",
                "*/",

                "/* this is a doc */",
                "public class Bar3",
                "{",
                    "private int i = 3;",
                "}",
            "}",

            "public class Bar4",
            "{",
                "public void foo(int i)",
                "{",
                    "doSomething()",
                "}",
            "}",
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 5)
        self.assertEquals(res[0].package, 'Foo1.Bar1')
        self.assertEquals(len(res[0].attributes), 2)
        self.assertEquals(len(res[0].methods), 1)
        self.assertEquals(res[0].attributes[0].name, 'instance')
        self.assertEquals(res[0].attributes[1].name, 'i')
        self.assertEquals(res[0].methods[0].signature, 'void foo()')

        self.assertEquals(res[1].package, 'Foo1.Bar1.Inner1')
        self.assertEquals(len(res[1].attributes), 1)
        self.assertEquals(len(res[1].methods), 1)
        self.assertEquals(res[1].attributes[0].name, 'i')
        self.assertEquals(res[1].methods[0].signature, 'void inner1()')

        self.assertEquals(res[2].package, 'Foo1.Bar1.Inner2')
        self.assertEquals(len(res[2].attributes), 0)
        self.assertEquals(len(res[2].methods), 0)

        self.assertEquals(res[3].package, 'Foo2.Bar3')
        self.assertEquals(len(res[3].attributes), 1)
        self.assertEquals(len(res[3].methods), 0)
        self.assertEquals(res[1].attributes[0].name, 'i')

        self.assertEquals(res[4].package, 'global.Bar4')
        self.assertEquals(len(res[4].attributes), 0)
        self.assertEquals(len(res[4].methods), 1)
        self.assertEquals(res[4].methods[0].signature, 'void foo(int i)')

    def test_special_names(self):
        ''' Checks what happens when the variables have special names. '''
        content = [
            "namespace namespace1 {",
                "public static class Myclass {",
                    "public void publicMethod() {",
                        "doSomething()",
                    "}",

                    "private static const final int constValue = 3;",
                "}",
            "}",
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 1)
        klass = res[0]
        self.assertEquals(klass.package, 'namespace1.Myclass')
        self.assertEquals(len(klass.methods), 1)
        self.assertEquals(len(klass.attributes), 1)
        self.assertEquals(klass.methods[0].signature, 'void publicMethod()')
        self.assertEquals(klass.attributes[0].name, 'constValue')

    def test_parse_enum(self):
        content = [
            "public class Normal",
            "{",
                "public enum Foo",
                "{",
                    "FIRST (1),",
                    "SECOND (2),",
                    "LAST (3);",

                    "private int k;",

                    "public Foo(int k) {",
                        "val = k",
                    "}",

                    "public int getK() {",
                        "return val",
                    "}",
                "}",

                "public enum Bar",
                "{",
                    "A,",
                    "B,",
                    "C;",
                "}",
            "}",
        ]
        res = self.parser.parse_content(self.filepath, content)
        self.assertEquals(len(res), 3)
        klass = res[1]

        self.assertTrue(isinstance(klass, Enum))
        self.assertEquals(len(klass.methods), 2)
        self.assertEquals(len(klass.attributes), 4)
        self.assertEquals(klass.attributes[0].name, 'FIRST')
        self.assertEquals(klass.attributes[0].referenced_class_package, 'global.Normal.Foo')
        self.assertEquals(klass.attributes[1].name, 'SECOND')
        self.assertEquals(klass.attributes[1].referenced_class_package, 'global.Normal.Foo')
        self.assertEquals(klass.attributes[2].name, 'LAST')
        self.assertEquals(klass.attributes[2].referenced_class_package, 'global.Normal.Foo')

        self.assertEquals(klass.attributes[3].name, 'k')
        self.assertEquals(klass.attributes[3].type, 'int')


        klass = res[2]
        self.assertTrue(isinstance(klass, Enum))
        self.assertEquals(len(klass.methods), 0)
        self.assertEquals(len(klass.attributes), 3)

        self.assertEquals(klass.attributes[0].name, 'A')
        self.assertEquals(klass.attributes[1].name, 'B')
        self.assertEquals(klass.attributes[2].name, 'C')

