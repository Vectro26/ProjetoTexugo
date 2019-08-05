# -*- coding: utf-8 -*-

"""
Initialize the database.
"""

import os
import logging

from pywebuml.app import db
from pywebuml.parsers.parser_factory import get_parser
from pywebuml.parsers.exceptions import ParserException


console_handler = logging.StreamHandler()
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(console_handler)





class ParserExecuter(object):
    ''' Class that check will files should be parsed, and
    if they should execute them to be parsed. Also saves the
    parsed data into the database.

    The attribute  `found` has the number of file that should be
    parsed, the `ignored` has the number of files that where ignored
    because of several reasons, and `errors` has the number of files
    that raise and exception while parsing them.

    The ignore files are the one that have a valid file extension (for
    example foo.cs) but the parsed didn't return any result.
    '''
    # Folders that should be ignored.
    IGNORE_FOLDERS = [
        '.svn',
        '.hg',
    ]

    # File types that should be ignored.
    VALID_FILE_EXTENSIONS = [
        'cs',
        'java'
    ]


    def __init__(self):
        ''' Initialize the counters to 0. Also, creates the database.
        '''
        self.found = 0
        self.ignored = 0
        self.error = 0
        db.create_all()


    def parse(self, base_folder_path):
        ''' Checks the folder and the files of the `base_folder_path`
        and parse the files.

        :parameters:
            `base_folder_path`: str
                the base folder from where start parsing the files.
        '''
        self.parse_folder(base_folder_path)
        LOGGER.info('Found %s files, where %s were ignored and %s could not be parsed' \
                        % (self.found, self.ignored, self.error))


    def parse_folder(self, folder_name):
        files = os.listdir(folder_name)
        files.sort()
        for name in files:
            full_path = os.path.join(folder_name, name)
            if os.path.isdir(full_path):
                if name not in self.IGNORE_FOLDERS:
                    self.parse_folder(full_path)
                else:
                    LOGGER.debug("Ignoring folder: %s", full_path)
            else:
                self.parse_file(full_path)


    def parse_file(self, filename):
        # get the last part of the file becuase the file can have
        # 2 or more . (for example: Asd.g.cs)
        # Ad-hoc for my work...
        file_extension = filename.split('.')[-1]
        if not file_extension in self.VALID_FILE_EXTENSIONS:
            LOGGER.debug("Ignore file: %s", filename)
            return None

        self.found += 1
        LOGGER.debug("Parsing file: %s", filename)
        try:
            parser_instance = get_parser(file_extension)
            res = parser_instance.parse(filename)
            if not res:
                self.ignored += 1
            for value in res:
                db.session.add(value)
            db.session.commit()
        except ParserException, e:
            self.error += 1
            LOGGER.exception("Problem while parsing file: %s", filename)
            db.session.rollback()
        except Exception, e:
            self.error += 1
            LOGGER.exception("Unknow exception while parsing file: %s", filename)
            db.session.rollback()


