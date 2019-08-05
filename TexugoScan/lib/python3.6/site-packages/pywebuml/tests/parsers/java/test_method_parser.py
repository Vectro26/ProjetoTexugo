# -*- coding: utf-8 -*-

'''
Has some test for `pywebuml.parsers.java.method_parser`
'''

from unittest2 import TestCase
from pywebuml.parsers.java.method_parser import JavaMethodParser


class TestJavaMethodParser(TestCase):

    def setUp(self):
        self.parser = JavaMethodParser()

    def test_skip_language_methods(self):
        ''' Test that the  Object methods aren't included.
        '''
        actual = self.parser.should_skip_language_methods('public String toString ()')
        self.assertTrue(actual)

        actual = self.parser.should_skip_language_methods('public String toString()')
        self.assertTrue(actual)

        actual = self.parser.should_skip_language_methods('public String myStringMethod()')
        self.assertFalse(actual)


