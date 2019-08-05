# -*- coding: utf-8 -*-

'''
Some tests for `pywebuml.parsers.utils.`
'''

from unittest2 import TestCase

from pywebuml.models import Class, Enum
from pywebuml.parsers.utils import has_any_keyword, remove_comments, \
                                   remove_keywords, get_visibility, \
                                   get_type_and_name

class UtilsTest(TestCase):


    def test_has_keyword(self):
        ''' Some basic tests for has keyword.
        '''
        self.assertTrue(has_any_keyword('this is KEYWORD', ['KEYWORD']))
        self.assertFalse(has_any_keyword('this is keyword', ['KEYWORD']))
        self.assertFalse(has_any_keyword('this is KEYWORDs', ['KEYWORD']))
        self.assertFalse(has_any_keyword('this isKEYWORD', ['KEYWORD']))


    def test_has_keyword_more_than_one(self):
        ''' Test what happens to has_keyword when using a list
        that has more than one element.
        '''
        self.assertTrue(has_any_keyword('KEY this is WORD', ['KEY', 'WORD']))
        self.assertTrue(has_any_keyword('KEY this is WORD', ['KEY', 'FOO']))
        self.assertTrue(has_any_keyword('KEY this is WORD', ['FOO', 'WORD']))
        self.assertFalse(has_any_keyword('KEY this is WORD', ['FOO', 'BAR']))


    def test_remove_comments_no_comments(self):
        ''' Test remove_comments when the content has no comments.
        '''
        content = [
            'public class Foo',
            '{',
            '}',
        ]
        expected = content
        actual = remove_comments(content)
        self.assertEquals(expected, actual)


    def test_simple_remove_comments(self):
        ''' Test to remove some javadocs and some commented lines.
        '''
        content = [
            '/* this is the class javadoc',
            '*',
            '***********/',
            'public class Foo {',

                '// this is the max value',
                'private int maxValue;',
            '}',
        ]
        expected = [
            'public class Foo {',
                'private int maxValue;',
            '}',
        ]
        actual = remove_comments(content)
        self.assertEquals(expected, actual)


    def test_remove_inline_comments(self):
        ''' Test what happens when the file has comments the same
        line there is code.
        '''
        content = [
            'public class Foo // extends Bar',
            '{',
                'private int j; // = 3;',

                'public Foo() {',
                    'if (this.j == 3 /* || this.j == 2 */) {',
                        'throw new RuntimeError("foo")',
                    '}',
                '}',

                'public/* static */Object getValue() {',
                    '/*',
                    'if (this.j == 3)',
                        'raise RuntimeException("getValue")',
                '*/ }',
            '}',
        ]

        expected = [
            'public class Foo',
            '{',
                'private int j;',

                'public Foo() {',
                    'if (this.j == 3 ) {',
                        'throw new RuntimeError("foo")',
                    '}',
                '}',

                'public Object getValue() {',
                '}',
            '}',
        ]
        actual = remove_comments(content)
        self.assertEquals(expected, actual)


    def test_remove_comments_when_nested(self):
        ''' Test what happens when the file has some nested comments.
        '''
        content = [
            'public class Foo {',
                '// private int i = 3; /*',
                'private int j = 4; // */',
                '/* // private int k = 5; */',
                '/* blah blah blah */ private int l = 6;',

                '/* // this is all commented',
                    '/*',
                        'public Foo() { }',
                '*/',
                '/// Writes a comment.  The comment characters /* */ or // should be included in the comment string',
            '}',
        ]

        expected = [
            'public class Foo {',
                'private int j = 4;',
                'private int l = 6;',
            '}',
        ]
        actual = remove_comments(content)
        self.assertEquals(expected, actual)


    def test_simple_remove_keywords(self):
        ''' Some simple tests for remove_keywords.
        '''
        actual = remove_keywords('public int foo = 3;', ['public'])
        self.assertEquals('int foo = 3;', actual)

        actual = remove_keywords('public int foo = 3;', ['staic'])
        self.assertEquals('public int foo = 3;', actual)

        actual = remove_keywords('public int myPublicValue = 3;', ['public'])
        self.assertEquals('int myPublicValue = 3;', actual)

        # I know this case isn't valid, but it is to test what
        # happens if the keyword is at the end of the line
        actual = remove_keywords('public int myPublicValue = static ;', ['static'])
        self.assertEquals('public int myPublicValue = ;', actual)

        actual = remove_keywords('public static int mystaticValue = 3;', ['static'])
        self.assertEquals('public int mystaticValue = 3;', actual)

        # I know this isn't valid but is used to check if the keyword is
        # removed all the times that is found.
        actual = remove_keywords('public static int mystaticValue = static ;', ['static'])
        self.assertEquals('public int mystaticValue = ;', actual)


    def test_remove_more_than_one_keyword(self):
        ''' Test removing more than one keyword.
        '''
        actual = remove_keywords('public static int foo = 3;', ['static', 'final'])
        self.assertEquals('public int foo = 3;', actual)

        actual = remove_keywords('public final int foo = 3;', ['static', 'final'])
        self.assertEquals('public int foo = 3;', actual)

        actual = remove_keywords('public static final int foo = 3;', ['static', 'final'])
        self.assertEquals('public int foo = 3;', actual)

        actual = remove_keywords('public int foo = 3;', ['static', 'final'])
        self.assertEquals('public int foo = 3;', actual)


    def test_check_visibility(self):
        ''' Test getting the visibility of a method or attribute.
        '''
        visibility = get_visibility('private int i = 3;')
        self.assertEquals('private', visibility)

        visibility = get_visibility('protected int i = 3;')
        self.assertEquals('protected', visibility)

        visibility = get_visibility('public int i = 3;')
        self.assertEquals('public', visibility)

        visibility = get_visibility('internal int i = 3;')
        self.assertEquals('private', visibility)

        visibility = get_visibility('int i = 3;')
        self.assertEquals('protected', visibility)


    def test_attribute_get_type_and_name(self):
        ''' Test some simple cases for get_type_and_name for attributes.
        '''
        class_model = Class('global.Foo', 'Foo', '/foo.java', 'Java')
        type, name = get_type_and_name('int i', 0, class_model)
        self.assertEquals(('int', 'i'), (type, name))

        type, name = get_type_and_name('String i', 0, class_model)
        self.assertEquals(('String', 'i'), (type, name))

        type, name = get_type_and_name('List<Integer> i', 0, class_model)
        self.assertEquals(('List<Integer>', 'i'), (type, name))

        type, name = get_type_and_name('Integer[] i', 0, class_model)
        self.assertEquals(('Integer[]', 'i'), (type, name))

        type, name = get_type_and_name('Integer []i', 0, class_model)
        self.assertEquals(('Integer[]', 'i'), (type, name))

        type, name = get_type_and_name('Dictionary<string, Foo>mValues', 0, class_model)
        self.assertEquals(('Dictionary<string,Foo>', 'mValues'), (type, name))



    def test_method_get_type_and_name(self):
        ''' Test some simple clases for get_type_and_name for methods.
        '''
        class_model = Class('global.Foo', 'Foo', '/foo.java', 'Java')
        return_type, name = get_type_and_name('void foo', 0, class_model)
        self.assertEquals(('void', 'foo'), (return_type, name))

        return_type, name = get_type_and_name('void foo', 0, class_model)
        self.assertEquals(('void', 'foo'), (return_type, name))


    def test_enums_get_type_and_name(self):
        ''' Test getting the type of an attribute of an enum.
        '''
        owner_model = Class('global.Foo', 'Foo', '/foo.java', 'Java')
        class_model = Enum('global.Foo.Days', 'Days',
                            './foo.java', 'Java', owner_model)
        type, name = get_type_and_name('MONDAY,', 0, class_model)
        self.assertEquals(('global.Foo.Days', 'MONDAY'), (type, name))





