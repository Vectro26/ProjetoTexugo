# -*- coding: utf-8 -*-

'''
Tests for pywebuml.initialize.parsers.csharp.method_parser:CSharpMethodParser
'''

from unittest2 import TestCase
from pywebuml.models import Class
from pywebuml.parsers.csharp.method_parser import CSharpMethodParser

class MethodParserTest(TestCase):


    def setUp(self):
        self.parser = CSharpMethodParser();
        self.class_model = Class('global', 'Foo', './foo.cs', 'C#')


    def test_clean_for_generic_methods(self):
        ''' Test for cleaning the generic conditions of the methods.
        '''
        signature = 'public T Foo(int bar) where T : new'
        actual = self.parser.clean_language_things(signature)
        self.assertEquals('public T Foo(int bar)', actual)

        signature = 'public T Foo2(T bar) where T : new'
        actual = self.parser.clean_language_things(signature)
        self.assertEquals('public T Foo2(T bar)', actual)

        signature = 'public T Foo3<T>() where T : new'
        actual = self.parser.clean_language_things(signature)
        self.assertEquals('public T Foo3()', actual)

        signature = 'public List<T> Foo4<T>()'
        actual = self.parser.clean_language_things(signature)
        self.assertEquals('public List<T> Foo4()', actual)

        signature = 'public List<T> Foo5<T> ()'
        actual = self.parser.clean_language_things(signature)
        self.assertEquals('public List<T> Foo5 ()', actual)

        signature = 'IEnumerable<KeyValuePair<T, U>> Foo6<T, U>()'
        actual = self.parser.clean_language_things(signature)
        self.assertEquals('IEnumerable<KeyValuePair<T, U>> Foo6()', actual)

    def test_clean_removing_base_constructors(self):
        ''' Test removing the call to the base constructor.
        '''
        signature = 'public Foo() : base(3)'
        actual = self.parser.clean_language_things(signature)
        self.assertEquals('public Foo()', actual)



    def test_parse_constructors_with_base(self):
        ''' Test parsing class constructors '''
        content = [
            "public Foo() : base(3)",
            "{",
                "doSomething()",
            "}",


            "public Foo() :",
                "base(3)",
            "{",
                "doSomething()",
            "}",

            "public Foo() : base(3) {",
                "doSomething()",
            "}",

            "public Foo(int bar) : base(bar) { }",
        "}"
        ]
        index, method = self.parser.parse(self.class_model, content, 0)
        self.assertEquals(index, 4)
        self.assertEquals(method.name, 'Foo')
        self.assertEquals(method.signature, 'Foo()')

        index, method = self.parser.parse(self.class_model, content, 4)
        self.assertEquals(index, 9)
        self.assertEquals(method.name, 'Foo')
        self.assertEquals(method.signature, 'Foo()')

        index, method = self.parser.parse(self.class_model, content, 9)
        self.assertEquals(index, 12)
        self.assertEquals(method.name, 'Foo')
        self.assertEquals(method.signature, 'Foo()')

        index, method = self.parser.parse(self.class_model, content, 12)
        self.assertEquals(index, 13)
        self.assertEquals(method.name, 'Foo')
        self.assertEquals(method.signature, 'Foo(int bar)')


    def test_skip_operators_methods(self):
        ''' Test that checks that the operator methods are skipped.
        '''
        content = [
            "public static bool operator !=(Foo foo1, Foo foo2)",
            "{",
                "return foo1.name != foo2.name",
            "}",
        "}",
        ]
        index, method = self.parser.parse(self.class_model, content, 0)
        self.assertEquals(index, 4)
        self.assertTrue(method is None)
