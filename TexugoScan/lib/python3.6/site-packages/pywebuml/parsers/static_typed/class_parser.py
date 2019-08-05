# -*- coding: utf-8 -*-

'''
Created on 12/03/2011

@author: tzulberti
'''

from logging import getLogger


from pywebuml.parsers.constants import CLASS_KEYWORDS, MODIFIERS
from pywebuml.parsers.exceptions import (
            MissingClosingClassDefinition,
            MissingOpeningClassDefinition
            )

from pywebuml.models import (
            Class,
            ClassInheritence,
            ClassImplements,
            Enum,
            Interface,
            Abstract
            )
from pywebuml.parsers.utils import (
            has_any_keyword,
            remove_keywords,
            get_visibility
            )

LOGGER = getLogger(__name__)


class AbstractStaticTypedClassParser(object):
    ''' Given a content it parses it content and returns the class
    representation.

    It has the following abstract methods:

    - get_attribute_parser: returns the parser that will be used when
      an attribute is found

    - get_method_parser: returns the method parser that will be used
      when a method is found.

    - get_class_definition_data: returns the data taken from the class
      signature. For example, the list of implemented classes, and interfaces.

    - is_other_type: identifies if the class is an special class of the
      language. For example, for C#, it can be an inner class.

    - get_other_type: gets the class based in the other types data.

    - get_programming_language: get the current language of the parser.

    - get_package_manager: get the instance of
      `pywebuml.static_typed.package_manager:PackageManager` that will be
      used to get the package of the referenced class and the one of the
      attrbitues. This instance will only be created once.
    '''

    def __init__(self, content):
        ''' Initialize the ClassParser with the following attributes:

        is_enum: bool
            indicates if the current class is an enum.
        is_abstract: bool
            indicates if the current class is abstract.
        is_interface: bool
            inidcates if the current class is an interface.
        language: str
            the current programming language.
        package_manager: `pywebuml.parsers.static_typed.package_manager:PackageManager`
            the instance used to get the full references of the classes.

        The attributes `is_enum`, `is_abstract`, and `is_interface` will be
        overriden for each parsed class. The rest of them arent.
        '''
        self.is_enum = False
        self.is_abstract = False
        self.is_interface = False
        self.language = self.get_programming_language()
        self.package_manager = self.get_package_manager(content)


    def get_package_manager(self, content):
        ''' Returns the instance of the package manager that will
        be used to get the refernced package of the parsing class,
        and the one of the attributes.

        :parameters:
            content: list(str)
                the content of the file once that it has been cleaned
                and removed the language specific things.

        :returns:
            the instance of the manager that will be used to get
            the data.
        '''
        raise NotImplementedError('get_package_manager')


    def get_programming_language(self):
        ''' Returns the language for the working parser.

        :returns:
            the name of the programming language that the parser
            parse. For example, C#, Java, etc...
        '''
        raise NotImplementedError('get_programming_language')


    def parse(self, filepath, content, index, owner = None):
        ''' Parse the content of the class.

        The index must be setted in the first line of the class definition.

        The result will be a list with more than one element if there is an
        inner class. If there is more than one class definition in the file,
        then this method should be used more than once.

        :parameters:
            filepath: str
                the folder and name of the file. For example:
                    ./examples/mycode.cs
            content: list(str)
                the content of the file.
            owner: pywebuml.model.Class
                the owner of this class. This will only be used if the class
                as inner.

        :return:
            a tuple with the index and the list of class representation. I
        '''
        res = []
        started_definition = index
        if not owner:
            base_class_package = self.package_manager.get_class_package(index)
        else:
            base_class_package = owner.package

        index, current_class = self.parse_class_signature(filepath, content,
                                             index, base_class_package, owner)
        res.append(current_class)
        position = index - 1

        current_line = content[position]
        if '{' in current_line and '}' in current_line and \
            has_any_keyword(current_line, CLASS_KEYWORDS):
            # then the class definition is of 1 line
            # For example:
            #   public class Foo { }
            return (index, res)

        while True:
            if index == len(content):
                raise MissingClosingClassDefinition(started_definition)


            current_line = content[index]
            if current_line in  ('}', '};'):
                # the closing key of the class definition
                # must comprare to equals because the current line could be a
                # one line method, attr or inner class definition
                index += 1
                break

            if has_any_keyword(current_line, CLASS_KEYWORDS):
                index, inner_res = self.parse(filepath, content, index, current_class)
                res.extend(inner_res)

            elif self.is_method(current_line, current_class):
                index = self.parse_method(content, index, current_class)
            else:
                index = self.parse_attribute(content, index, current_class)

        return (index, res)


    def parse_attribute(self, content, index, current_class):
        ''' Parse the atttibute.

        :parameters:
            content: list(str)
                the content of the file.
            index: int
                the current line of the content
            current_class: pywebuml.models.Class
                where the attribute belongs.

        :returns:
            the index where the attribute definition ends.
        '''
        index, attr = self.get_attribute_parser().parse(current_class,
                                content, index, self.package_manager)
        return index


    def get_attribute_parser(self):
        ''' Returns the attribute parses.

        :returns:
            an instance of `pywebuml.parsers.AttributeParser` that will be used
            to parse the found attribute.
        '''
        raise NotImplementedError('get_attribute_parser')


    def parse_method(self, content, index, current_class):
        ''' The same as parse_attribute but this time with a method.
        '''
        index, method = self.get_method_parser().parse(current_class, content, index)
        return index


    def get_method_parser(self):
        ''' Returns the method parser.

        :returns:
            an instance of `pywebuml.parsers.MethodParser` that will be used
            to parse the method definition.
        '''
        raise NotImplementedError('get_method_parser')



    def parse_class_signature(self, filepath, content, index,
                                    base_class_package, owner = None):
        ''' Returns the `pywebuml.models.Class`  object without any attribute
        or method, but with its implementations and extensions.

        :parameters:
            content: list(str)
                the content of the file
            index: int
                from which position of the content start getting the info.
            base_class_package: str
                the base class package that will be used with the class name
                to get the complete package of the class.
            owner: `pywebuml.models.Class`
                if the class is an inner class, then this is the
                parent class.

        :returns:
            a ``pywebuml.models.Class`` taking into account the
            content of the file.
        '''
        current_line = content[index]

        self.is_interface = has_any_keyword(current_line, ['interface'])
        self.is_abstract = has_any_keyword(current_line, ['abstract'])
        self.is_enum = has_any_keyword(current_line, ['enum'])
        is_other_type = self.is_other_type(current_line)

        class_data = remove_keywords(current_line, CLASS_KEYWORDS)
        class_data = remove_keywords(class_data, MODIFIERS)


        visibility = get_visibility(class_data)
        class_data = remove_keywords(class_data, [visibility])


        # if the class definition doesn't end in that line then
        # it might have some other base_classes in the following lines
        # for example:
        #   public class Foo : A, B, C
        #                      D, E, F
        #                      G {
        finish = False
        current_line = class_data
        class_definition = ''
        current_position = index

        while True:
            current_position += 1
            class_definition += current_line

            # found the end of the class definition
            if '{' in current_line:
                break

            if current_position == len(content):
                raise MissingOpeningClassDefinition()

            current_line = content[current_position].strip()



        # removes that it at the right of the  { becuase
        # that belongs to the class implementation
        class_definition = class_definition[:class_definition.index('{')]

        class_name, base_classes, implemented_interfaces = \
                    self.get_class_definition_data(class_definition, content)

        index = current_position
        LOGGER.debug("Found class: %s", class_name)
        package = '%s.%s' % (base_class_package, class_name)

        # TODO ver como manejar el tema de partial
        if is_other_type:
            klass = self.get_other_type_class_model(package, class_name,
                                    filepath, self.language,
                                    owner)
        else:
            klass = self.get_class_model(package, class_name,
                              filepath, self.language, owner)

        for base_package in base_classes:
            ClassInheritence(klass, base_package)

        for interface_package in implemented_interfaces:
            ClassImplements(klass, interface_package)

        return (index, klass)


    def is_other_type(self, current_line):
        ''' Identifies if the class definition is a type specific for
        the programming language.

        :parameters:
            current_line: str
                the definition of the class.

        :returns:
            False (default) is the class is an interface, enum, etc.. or
            True if it is specific for the programming language.
        '''
        return False


    def get_class_definition_data(self, class_definition, content):
        ''' Returns the parsed data of the class name.

        For example, for the following text::

            import org.pywebuml.Bar
            import org.pywebuml.IFoo

            public class Foo extends Bar implements IFoo

        the `class_name` will be only Foo, and the base_classes
        will be [`org.pywebuml.Bar`], and implemented_interfaces
        will be [`org.pywebuml.IFoo`].

        :returns:
            a tuple(str, list(str), list(str)) where the first
            value is the name of the class, the second one, is the
            package of the base classes, and the last one is the package
            of the interfaces that the class implements.
        '''
        raise NotImplementedError('get_class_definition_data')


    def is_method(self, current_line, current_class):
        ''' Identifies if the current line is a method
        or an attribute.

        :parameters:
            content: list(str)
                the content of the file
            current_class: `pywebuml.models.Class`
                the current class that is being parsed.

        :returns:
            True if the current line is a method definition
            else False.
        '''
        if not '(' in current_line:
            # it is an attribute (or the properties) because all methods must
            # have a () in the definition.
            return False

        if '=' in current_line and '{' not in current_line:
            # it is an attribute:
            #   private int b = 3;
            return False

        if '(' in current_line and '=' in current_line and (
                current_line.find('(') > current_line.find('=')
                ):
            # in this case the value is something like:
            #   private Foo[] bar = new Foo[] { new Foo(1,2) };
            return False
        elif isinstance(current_class, Enum):
            # check it is is an attr with a value or if it is a
            # method. For example, take into account the following
            # cases:
            #   FIRST (1),
            #   myMethod (int j)
            # this is to take if it has (. If it doesn't it will
            # use one of the cases above.
            if '{' in current_line:
                return True
            else:
                # TODO the { could be in the next line...
                return False

        else:
            return True


    def get_other_type_class_model(self, package, class_name,
                             filepath, language, owner):
        ''' Returns the model based in the current data of the language.

        :parameters:
            all the data to create the class instance.

        :returns:
            an instance of `pywebuml.models.Class` based in the data.
        '''
        raise NotImplementedError('get_other_class_model')


    def get_class_model(self, package, class_name,
                           filepath, language, owner = None):
        ''' Returns the class model base on the data, and
        taking into account the type of class it is.

        :parameters:
            package, class_name, filepath, language: str
                the data of the class.
            owner: `pywebuml.model.Class`
                the class in which the current class was found.

        :returns:
            a `pywebuml.model.Class` instance based in the data, and
            in the type of class.
        '''
        if self.is_enum:
            klass = Enum(package, class_name,
                                filepath, language, owner)
        elif self.is_interface:
            klass = Interface(package, class_name, filepath,
                                    language, owner)
        elif self.is_abstract:
            klass = Abstract(package, class_name, filepath,
                                    language, owner)
        else:
            klass = Class(package, class_name,
                                    filepath, language, owner)
        return klass



