# -*- coding: utf-8 -*-

''' Gets the parser by the extension of the file.
'''

from pywebuml.parsers.csharp.file_parser import CSharpFileParser
from pywebuml.parsers.java.file_parser import JavaFileParser


def get_parser(file_extension):
    ''' Given a file extension, returns the parser for the file.

    :parameters:
        file_extension: str
            the extension of the file that is being parsed.

    :returns:
        the `pywebuml.parsers.FileParser` that will be used for
        that file.
    '''
    if file_extension == 'cs':
        return CSharpFileParser()
    elif file_extension == 'java':
        return JavaFileParser()
