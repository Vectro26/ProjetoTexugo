# -*- coding: utf-8 -*-

'''
Has the definition of the base parser that all the other parsers must extend.
'''

import codecs

class BaseParser(object):
    ''' Has some common method used by all the other parers.
    '''

    def parse(self, filename):
        ''' Will call ``parse_content`` with the content of the file.

        :parameters:
            filename: str
                the path and name of the file that should be parsed.
                For example:
                    /foo/bar/a.py
        '''
        # this can be done because usually the files don't have
        # more than 5000 lines.
        file_content = self.read_file(filename)
        file_content = self.clear_content(file_content)

        return self.parse_content(filename, file_content)

    def read_file(self, filename):
        ''' Reads the content of the file.

        :parameters:
            filename: str
                the path and name of the file to read.

        :returns:
            the content of the file.
        '''
        try:
            tmp = None
            tmp = open(filename)
            header = tmp.read(4)
        finally:
            if tmp:
                tmp.close()

        encodings = [
            (codecs.BOM_UTF32, 'utf-32'),
            (codecs.BOM_UTF16, 'utf-16'),
            (codecs.BOM_UTF8, 'utf-8'),
        ]
        open_encoding = None
        for bom, encoding in encodings:
            if header.startswith(bom):
                open_encoding = encoding
                break

        try:
            # the file is an utf-X file, so it should open
            # with codecs so the unicode content of that file
            # is returned.
            if open_encoding:
                f = codecs.open(filename, 'r', open_encoding)
                content = f.readlines()
                # removes the encoding part of the file, and converts encoded
                # chars to its values.
                content[0] = content[0].replace(bom.decode(open_encoding), '')
                #content = [c.decode(open_encoding) for c in content]
            else:
                # the file doesn't has a specific encoding,
                # so using the normal opening
                f = open(filename, 'r')
                content = f.readlines()
        finally:
            f.close()

        return content



    def clear_content(self, file_content):
        ''' Removes the empty lines from thye file, and strips all the lines.
        Also removes all the tabs.

        :parameters:
            file_content: list(str)
                the content of the file.

        :returns:
            the file content cleared.
        '''
        filtered_content = map(lambda l: l.replace("\t", ' '), file_content)
        filtered_content = filter(lambda l: l.strip(), filtered_content)
        filtered_content = map(lambda l: l.strip(), filtered_content)
        return filtered_content

    def parse_content(self, content):
        ''' Parse the content of the file and returns it
        converted into models.

        :parameters:
            content: list(str)
                the content of the file. This content won't have
                empty lines, becuase those have been already removed.

        :returns:
            a list of ``pywebuml.models.Class`` with all the
            references setted.
        '''
        # TODO hacer de esta clase una abstracta.
        raise NotImplementedError("This method should be override")



