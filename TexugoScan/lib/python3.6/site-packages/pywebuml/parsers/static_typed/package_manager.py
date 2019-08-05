# -*- coding: utf-8 -*-

'''
Package manager definition

@author: tzulberti
'''

class AbstractPackageManager(object):
    ''' Defines the interface of the package manager.
    '''

    def __init__(self, content):
        ''' Initialize the manager using the cleaned content of the file.

        :parameters:
            content: list(str)
                the cleaned content of the file.
        '''
        pass

    def get_class_package(self, index):
        ''' Returns the package of the class definition that starts
        in the position index.

        :parameters:
            index: int
                the position in which the class definition was found.
                It will be a position of the content.

        :returns:
            an str that will be the base package for the class definition
        '''
        raise NotImplementedError('get_package_of_class_definition')


    def get_package_for_type(self, variable_type):
        ''' Returns the package of the referenced class. In this case, the
        current class definiton has an attribute of the type `variable_type`.
        For example::

            public class Foo {
                public Bar myAttr;
            }

        In this case, `variable_type` will be `Bar`.

        :parameters:
            class_name: str
                the referenced class name.

        :returns:
            the complete package definition of the referenced class.
        '''
        raise NotImplementedError('get_package_of_referenced_class')



