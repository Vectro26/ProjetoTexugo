# -*- coding: utf-8 -*-
'''
Attribute parser for static typed languages.

@author: tzulberti
'''

from logging import getLogger

from pywebuml.models import Attribute, Enum
from pywebuml.parsers.utils import (
                    get_visibility,
                    has_any_keyword,
                    remove_keywords,
                    get_type_and_name
                    )
from pywebuml.parsers.constants import (
                    CONST_KEYWORDS,
                    LANGUAGE_BASE_VALUES,
                    MODIFIERS,
                    )
from pywebuml.parsers.exceptions import (
                    ClossingArrayException,
                    )

LOGGER = getLogger(__name__)


class AbstractStaticTypedAttributeParser(object):
    ''' Given the class and the content of the file, it has the responsability
    of parsing it into a `pywebuml.models.Attribute``.

    It doesn't has abstract methods, but it has the method:
    - `should_skip_language_attributes` that should be overriden to take into
       account specific language things.
    '''

    def parse(self, class_model, content, index, package_manager):
        ''' Parse the method of the class of the content.

        :parameters:
            class_model:  ``pywebuml.model.Class``
                the current class that is being parsed.
            content: list(str)
                the content of the file
            index: int
                from where start parsing
            package_manager: `pywebuml.parsers.static_typed.package_manager`
                the package manager to use to get the referenced class
                complete path.

        :return:
            a tuple (pywembuml.models.Method, int) that has the parsed
            method and the index value from where it should continue reading.

        :raises:
           - `pywebuml.initialize.parser.exceptions.ClossingArrayException`
              if it can't find the closing } of the array definition

           - `pywebuml.initialize.parser.exceptions.EmptyAttributeNameException`
              if it cant get the name of the attribute.
        '''
        current_position = index
        current_line = content[index]

        visibility = get_visibility(current_line)
        is_static = has_any_keyword(current_line, ['static'])
        is_final = has_any_keyword(current_line, CONST_KEYWORDS)

        current_line = remove_keywords(current_line, MODIFIERS)

        # iterate the property methods of the attribute.
        if self.should_update_index(current_line, content, current_position, class_model):
            opened_keys = 0
            opened_parenthesis = 0
            found_equals = False

            # before starting checking unitl which position, the index should
            # move, it check from where it should start.
            if (current_line.endswith('=') or '=' not in current_line) \
                    and not '{' in current_line:
                # in this case, the line should be changed because the value
                # is in the current line. For example:
                #       private i =
                #               3;
                current_position += 1

            elif '{' not in current_line and content[current_position + 1].startswith('{'):
                # This is the case of an array definition. For example
                #       private int[] k = new int[]
                #           { 1, 2, 3 }
                current_position += 1


            while True:
                if current_position == len(content):
                    # TODO change the value of this because this isn't only for arrays...
                    raise ClossingArrayException(index)

                line = content[current_position]
                opened_keys = opened_keys + line.count('{') - line.count('}')
                opened_parenthesis = opened_parenthesis + line.count('(') - line.count(')')
                current_position += 1

                if opened_keys == 0 and opened_parenthesis == 0 and (
                        line.endswith(';') or line.endswith('}')):
                    # this is for cases like:
                    #   private String text = "This is a long text" +
                    #           "this continues here" +
                    #           "and finally ends here";
                    # the endswith } is for taking into account C# properties.
                    # TODO remove this from here it take it into c# parser.
                    break

        current_line = self.clean_line(current_line)
        if self.should_skip_language_attributes(current_line):
            if current_position == index:
                current_position += 1
            return (current_position,  None)

        # can't use current_line.split(' '), becuase there can be more than
        # one space between the type and variable definition
        variable_type, name = get_type_and_name(current_line,
                                                    index,
                                                    class_model)
        referenced_class_package = self.get_referenced_type(variable_type, package_manager)


        if index == current_position:
            # in this case the variable is of 1 line...
            #       private int j;
            current_position += 1

        LOGGER.debug("Found attribute: %s", name)
        return (current_position,
                Attribute(name, variable_type, class_model, visibility,
                            is_static, is_final, referenced_class_package)
                 )


    def should_update_index(self, current_line, content, current_position, class_model):
        ''' Checks if the index of the file should be moved more than
        one position. This is used when the attribute is defined in more
        than line. For example::

            private int[] foo = new int[] {
                        1,
                        2
                        }
            private Foo foo = new Foo(
                                    new Bar(),
                                    2)

        :parameters:
            current_line: str
                the current line that is being parsed.
            current_position: int
                the current position of the content that is being parsed.
            content: list(str)
                the cleaned content of the file.
            class_model: `pywebuml.models.Class`
                the current class where the attribute belongs.

        :returns:
            True if it index should move more than line, False if the
            attribute is defined in one line.
        '''
        should_iterate = False
        if isinstance(class_model, Enum) and \
                (current_line.endswith(';') or current_line.endswith(',') or
                        class_model.programming_language == 'C#'):
            # TODO check in C# if the value of an ENUM can be defined
            # in more than one line.
            # in this case the line is an attribute
            # of an enum that shouldn't be iterated.
            should_iterate = False
        elif not current_line.endswith(';') and \
                not '{' in current_line and \
                not '(' in current_line:
            # iterate if there is not '(' or '{' but the
            # **;** wasn't found at the end of the line.
            should_iterate = True;

        elif current_line.count("{") != current_line.count("}"):
            # the array definition starts here but it doesn't
            # ends in the same line.
            should_iterate = True

        elif current_line.count('(') != current_line.count(')'):
            # then the property uses the constructor of a class
            # that doesn't ends in the same line.
            # TODO add test case
            should_iterate = True;

        elif current_position < len(content) - 1:
            # only check if the next line is a property or set the values
            # of the array, if there are more lines in the content.

            current_position += 1
            if content[current_position].startswith('{'):
                # take into account that is an array. For example:
                #   public int[] i =
                #       { 3, ...
                should_iterate = True
            elif content[current_position].startswith('=') or content[current_position-1].endswith('='):
                # take into account values setted in the next line.
                # private List<Foo> foos
                #       = new ArrayList<Foo>();
                # TODO agregar un test para el caso:
                # private List<Foo> foos =
                #       new ArrayList<Foo>();
                should_iterate = True

        return should_iterate


    def clean_line(self, current_line):
        ''' Cleans the line from some language specific things.
        For example, in C# the line can have properties:

            public int i { get { return j } set { j = value } }

        :parameters:
            current_line:
                the line to remove the specific language things.

        :return:
            the cleaned line.
        '''
        if '=' in current_line:
            # then the line is something of the type:
            #   private Foo bar = new Foo();
            # Have to remove the things that are at the right from
            # the "="
            current_line = current_line[:current_line.index("=")]

        current_line = current_line.replace(';', '')
        current_line = current_line.strip()
        return current_line


    def should_skip_language_attributes(self, current_line):
        ''' Checks that some lines that are detected as attributes
        should be ignored. This lines belong to language specific things.
        For example, in C#:
            this[]

        :returns:
            true if the current line should be skipped, else False (default)
        '''
        return False


    def get_referenced_type(self, variable_type, package_manager):
        ''' Get the referenced type of the variable.

        :parameters:
            variable_type: str
                the type as defined when defined the variable. For example::

                    private int j;
                    private List<Foo> foos;

            package_manager: `pywebuml.parsers.static_typed.package_manager`
                the instance of the package manager used to get the
                complete path of the referenced class.

        :returns:
            the referenced class package, or None if the type is a base type.
        '''
        referenced_class_package = None

        if variable_type not in LANGUAGE_BASE_VALUES \
                and not '[' in variable_type and not '<' in variable_type:
            # its a common object attr. For example: Foo foo.
            referenced_class_package = variable_type

        elif '<' in variable_type:
            # it is a dictionary or list (some kind of template). For example:
            #   Map<Foo, int> or
            #   List<Foo>
            #   Map<Foo, List<Bar>> or
            #   List< MyTemplate<Foo>>
            # lets get the referenced classses that are in the dictionary.
            template_values = self._get_template_values(variable_type)

            for type in template_values:
                res = self.get_referenced_type(type, package_manager)
                if res:
                    return res
            return None

        elif '[' in variable_type:
            # it's an array type...
            array_class = variable_type[variable_type.index('[')+1: variable_type.index(']')].strip()
            if not array_class not in LANGUAGE_BASE_VALUES:
                referenced_class_package = variable_type

        if referenced_class_package and not '.' in referenced_class_package:
            referenced_class_package = package_manager.get_package_for_type(referenced_class_package)

        return referenced_class_package


    def _get_template_values(self, variable_type):
        ''' Given a variable type that uses Generics, return the generic class
        used. For example:
            List<Foo> will return ['Foo'],
            Dictionary<string, List<Foo>> will return ['string', 'List<Foo>']

        :parameters:
            variable_type: str
                a variable type that uses genercis.

        :returns:
            a list of str of the classes referenced in the variable type. Those
            clases could also be generics.
        '''
        template_values = variable_type[variable_type.index('<')+1: variable_type.rindex('>')].strip()
        template_values = template_values.split(',')
        res = []
        index = 0
        while index < len(template_values):
            if '<' not in template_values[index]:
                # the it is a class name (Foo, string, int, etc..)
                res.append(template_values[index].strip())
            elif template_values[index].count('<') == template_values[index].count('>'):
                # then it is a class that
                res.append(template_values[index].strip())
            else:
                # then the template_values is something like:
                #   ['string', 'SortedDict< string', 'Foo>']
                # when the type was:
                #   Dictionary<string, SortedDict<string, 'Foo'>
                opened_templates = template_values[index].count('<') - template_values[index].count('>')
                current_type =''
                while opened_templates != 0:
                    if current_type:
                        current_type += ','
                    current_type += template_values[index]

                    index += 1
                    opened_templates += template_values[index].count('<') - template_values[index].count('>')

                current_type += ',' + template_values[index]
                res.append(current_type.strip())

            index += 1

        return res




