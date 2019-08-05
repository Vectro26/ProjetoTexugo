# -*- coding: utf-8 -*-

"""
Has the different commands used by the application.
"""

import argparse
import logging
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(choices=['web', 'initialize', 'delete_tmpfiles'],
                        dest='program')

    args = parser.parse_args()
    if args.program == 'initialize':
        logging.basicConfig(level=logging.INFO, filename = 'initialize.log', filemode='w')
        from pywebuml.parsers.main import ParserExecuter
        parser = ParserExecuter()
        parser.parse('.')

    if args.program == 'web':
        # TODO encontrar alguna solucion mejor que este hack feo al logging
        logging.basicConfig(level=logging.INFO)
        from pywebuml.web import start_app
        start_app()

    if args.program == 'delete_tmpfiles':
        logging.basicConfig(level=logging.INFO)
        logging.info("Deliting images and dot files.")
        current_path = os.path.abspath(os.path.dirname(__file__))
        tmp_dir = os.path.join(current_path, 'static', 'tmp_dir')
        for filename in os.listdir(tmp_dir):
            os.remove(os.path.join(tmp_dir, filename))


