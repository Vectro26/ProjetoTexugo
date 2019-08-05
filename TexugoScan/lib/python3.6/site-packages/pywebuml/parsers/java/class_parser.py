# -*- coding: utf-8 -*-

'''

@author: tzulberti
Created on 13/03/2011
'''

from pywebuml.parsers.static_typed.class_parser import AbstractStaticTypedClassParser
from pywebuml.parsers.java.attribute_parser import JavaAttributeParser
from pywebuml.parsers.java.method_parser import JavaMethodParser
from pywebuml.parsers.java.package_manager import JavaPackageManager
from pywebuml.parsers.utils import has_any_keyword

class JavaClassParser(AbstractStaticTypedClassParser):
    '''
    '''

    def get_attribute_parser(self):
        return JavaAttributeParser()

    def get_method_parser(self):
        return JavaMethodParser()

    def get_programming_language(self):
        return 'Java'

    def get_package_manager(self, content):
        return JavaPackageManager(content)

    def is_other_type(self, current_line):
        return False

    def get_class_definition_data(self, class_definition, content):
        ''' Returns the class_name, interfaces, and base classes.
        In this case, it will use the content to search for the base
        and interfaces classes packages.

        :see:
            `AbstractStaticTypedClassParser`.get_class_definition_data
        '''
        class_name = []
        base_classes = []
        implemented_interfaces = []

        # TODO check which keyword is first: the extends or implements
        # TODO check if in Java is required that base clasess should
        # go before implemented classes.
        if has_any_keyword(class_definition, ['implements']):
            # the +12 is because len(' implements ') == 12
            implementations_data = class_definition[class_definition.index(' implements ') + 12:]

            # remove the implements part of the class_definitions
            class_definition = class_definition[:class_definition.index(' implements ')]
            for implemented_class in implementations_data.split(','):
                implemented_interfaces.append(self.get_class_package(implemented_class.strip(), content))

        if has_any_keyword(class_definition, ['extends']):
            # the +9 is becuase len(' extends ') == 9
            # TODO there could be a problem with this and template values....
            base_data = class_definition[class_definition.index(' extends ') + 9:]
            class_definition = class_definition[:class_definition.index(' extends ')]
            for base_class in base_data.split(','):
                base_classes.append(self.get_class_package(base_class.strip(), content))

        class_name = class_definition.strip()
        return class_definition, base_classes, implemented_interfaces



    def get_class_package(self, class_name, content):
        ''' Get the complete pacakge of the current class_name.

        If the class isn't imported the returned class_name will
        be the class_name
        '''
        return self.package_manager.get_package_for_type(class_name)
