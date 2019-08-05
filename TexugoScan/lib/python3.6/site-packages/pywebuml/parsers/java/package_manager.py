# -*- coding: utf-8 -*-

'''
Package Manager for java files.
'''

from pywebuml.parsers.static_typed.package_manager import AbstractPackageManager
from pywebuml.parsers.utils import has_any_keyword, remove_keywords

class JavaPackageManager(AbstractPackageManager):
    ''' Package manager for Java files.
    '''

    def __init__(self, content):
        self.current_package = ''
        self.classes_packages = dict()
        self._get_data(content)

    def _get_data(self, content):
        ''' Parse the file to identify the package for each class.
        '''
        for line in content:
            if has_any_keyword(line, ['package']):
                package = remove_keywords(line, ['package'])
                package = package.replace(';', '')
                self.current_package = package
            elif has_any_keyword(line, ['import']):
                import_data = remove_keywords(line, ['import'])
                import_data = import_data.replace(';', '')
                if not import_data.endswith('*'):
                    class_name = import_data.rsplit('.', 1)[1]
                    self.classes_packages[class_name] = import_data


    def get_class_package(self, index):
        return self.current_package

    def get_package_for_type(self, variable_type):
        ''' Returns the package for the variable_type.
        If there is an import of that type, then return that value.
        If not, and if the current definition is defined inside a package,
        then use that package. If there is no package, then return the name
        of the class.

        :parameters:
            variable_type: str
                the type for which search the package.

        :returns:
            the complete package for that type.
        '''
        if self.current_package:
            default = '%s.%s' % (self.current_package, variable_type)
        else:
            default = variable_type
        return self.classes_packages.get(variable_type, default)
