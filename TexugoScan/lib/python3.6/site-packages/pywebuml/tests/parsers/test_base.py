# -*- coding: utf-8 -*-

"""
Some basic tests for ``pywebuml.initializa.parsers.base:BaseParser``
"""
import codecs
import os
from unittest2 import TestCase

from pywebuml.parsers.base import BaseParser

class BaseParserTest(TestCase):


    def setUp(self):
        self.parser = BaseParser()

    def tearDown(self):
        if os.path.exists('tmp.cs'):
            os.remove('tmp.cs')

    def test_clear_content(self):
        """ Test that the clear_content cleans the file.
        """
        content = [
            " First Line ",
            "\t\t Second Line ",
            " ",
            "",
            "123ThirdLine",
            "LastLine \t\t",
            "\t",
        ]
        expected = [
            "First Line",
            "Second Line",
            "123ThirdLine",
            "LastLine"
        ]

        self.assertEquals(self.parser.clear_content(content),
                        expected)

    def test_read_utf8_file(self):
        """ Test what happens when reading an utf-8 encoded file.
        """
        content = [
            "public class MyClass\n",
            "{\n",
                u'This is unicode\n',
            "}\n",
        ]
        f = codecs.open('tmp.cs', 'w', 'utf-8')
        f.write(codecs.BOM_UTF8.decode('utf-8'))
        f.writelines(content)
        f.close()

        readed_content = self.parser.read_file('tmp.cs')
        self.assertEquals(readed_content, content)

        # TODO missing to delete tmp.cs file

    def test_replace_tabs_for_spaces(self):
        content = [
            "public class MyClass",
            "{",
                "\tprivate int\tmyAttr",
            "}",
        ]
        expected = [
            "public class MyClass",
            "{",
                "private int myAttr",
            "}",
        ]
        self.assertEquals(self.parser.clear_content(content),
                        expected)
