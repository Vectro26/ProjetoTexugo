# -*- coding: utf-8 -*-

'''
Created on 05/02/2011

@author: tzulberti
'''

from logging import getLogger

from pywebuml.app import db
from pywebuml.models import Class
from pywebuml.parsers.static_typed.class_parser import AbstractStaticTypedClassParser
from pywebuml.parsers.csharp.attribute_parser import CSharpAttributeParser
from pywebuml.parsers.csharp.method_parser import CSharpMethodParser
from pywebuml.parsers.csharp.package_manager import CSharpPackageManager
from pywebuml.parsers.utils import (
                has_any_keyword,
                )

LOGGER = getLogger(__name__)

class CSharpClassParser(AbstractStaticTypedClassParser):
    ''' Class parser for C# files.
    '''

    def get_programming_language(self):
        return 'C#'


    def get_attribute_parser(self):
        return CSharpAttributeParser()


    def get_method_parser(self):
        return CSharpMethodParser()

    def get_package_manager(self, content):
        return CSharpPackageManager(content)


    def is_other_type(self, current_line):
        ''' Returns true if the class is partial.
        '''
        return has_any_keyword(current_line, ['partial'])


    def get_other_type_class_model(self, package, class_name,
                                    filepath, language, owner):
        ''' Returns the model of the database when the class is partial.
        If the model isn't found, then it will use the method
        `get_class_model`
        '''
        res = self.find_partial_class(package)
        if not res:
            res = self.get_class_model(package, class_name,
                                       filepath, language, owner)
        return res


    def find_partial_class(self, package):
        ''' Find the database class that is defined with that package.
        If there is no definition, then it returns None.

        :parameters:
            package: str
                the full name of the class (global.Foo)

        :returns:
            the `pywebuml.model.Class` defined for that package.
        '''
        # Can't use Class.query because isn't inside a request.
        # see: http://flask.pocoo.org/mailinglist/archive/2010/10/14/flask-sqlalchemy-query-property
        query = db.session.query(Class)
        query = query.filter_by(package = package)
        return query.first()



    def get_class_definition_data(self, class_definition, content):
        ''' Returns the interfaces, base class and class name of the
        class_definition. All the packages of the interfaces and of the
        base class will always be **global**.

        :see:
            `AbstractStaticTypedClassParser`.get_class_definition_data
        '''
        implemented_interfaces = []
        base_classes = []
        class_name = ''

        if ':' in class_definition:
            class_name = class_definition[:class_definition.index(':')]
            are_template_constrains = False

            # check if the class is a singlton, and
            # the template might have some constrains.
            if '<' in class_name:
                # in this case is a template that has some constrains
                # TODO falta testear...
                if has_any_keyword(class_name, ['where']):
                    #TODO keyword bug....
                    class_name = class_name[:class_name.index('where')].strip()
                    are_template_constrains = True

            if not are_template_constrains:
                class_extensions = class_definition[class_definition.index(':') + 1 :].strip()
                for extension in class_extensions.split(','):
                    extension = extension.strip()
                    if extension.startswith('I'):
                        # TODO falta checkear que la segunda palabra tambien sea
                        # una mayuscula
                        implemented_interfaces.append('global.%s' % extension)
                    else:
                        base_classes.append('global.%s' % extension)
        else:
            class_name = class_definition

        class_name = class_name.strip()
        return class_name, base_classes, implemented_interfaces


    def is_method(self, current_line, current_class):
        ''' Overrides the is method to take into account that
        the line could be an operator definition, or the
        properties of an attribute.

        :parameters:
            content: list(str)
                the content of the file
            current_class: `pywebuml.models.Class`
                the current class that is being parsed.

        :returns:
            True if the current line is a method definition
            else False.
        '''
        if has_any_keyword(current_line, ['operator']):
            # Take into account if the line is an operator definition.
            #   public static bool operator !=(Foo lhs, Foo rhs)
            return True

        # check if it is a method defined in one line
        # or the properties (rare which has a method that uses (
        # of the attribute. For example:
        #    public OnDemand() { b = 3; }
        #    public int attr { get { Debug.Log("Foo"); value; } }
        elif has_any_keyword(current_line, ['get', 'set']):
            return False
        else:
            return super(CSharpClassParser, self).is_method(current_line,
                                  current_class)
