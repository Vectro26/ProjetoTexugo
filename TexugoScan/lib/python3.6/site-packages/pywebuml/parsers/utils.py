# -*- coding: utf-8 -*-

"""
Has the different parsers used to get the data from a programming file.
"""


from pywebuml.models import VISIBILITY_VALUES, Enum
from pywebuml.parsers.exceptions import (
                    EmptyNameException,
                    )


def has_any_keyword(current_line, keywords):
    ''' Search if the current_line has any of the keywords.

    :parameters:
        current_line: str
            the current line of the file
        keywords: list(str)
            the keywords to search in the line

    :returns:
        True if the current_line has any of the keywords, else False.
    '''
    # it has to be splited and can't check for each word to take
    # into account the name of the attribute or method. For example:
    #   public int myMethodclass();
    data = current_line.split(' ')
    data = map(lambda l: l.strip(), data)
    for keyword in keywords:
        if keyword in data:
            return True
    return False



def remove_comments(content):
    ''' Removes the documentation of the content. It will
    remove all the documents of the content. For example, if
    the content is::

        >>> content = [
            "// this is a comment",
            "public class Foo {",
                "private int min; //this is the min value",

                "/** this is where the javadoc begins",
                "*/",
                "public void foo() {"
                    return /* this_is_some_value */;
                "}"
            "}",
            ]
        >>> '\n'.join(remove_comments(content))
        "public class Foo {"
            "private int min;"
            "public void foo() {"
                "return ;"
            "}"
        "}"

    :parameters:
        content: list(str)
            the content of the read file.

    :returns:
        the new content (list(str)) without the comment blocks
        and lines.
    '''
    position = 0
    res = []
    while True:
        line = content[position]
        line_comment_position = line.find('//')
        if line_comment_position >= 0:
            # Some text of the line might have usefull information
            # So I am getting that value. For example:
            #       private int max; // the max value
            has_block = '*/' in line and '/*' in line
            block_begins = line.find('/*')
            line = line[: line_comment_position].rstrip()
            if has_block and block_begins < line_comment_position:
                # take into account this special case:
                #   /* // this is a comment inside a comment block */
                # but not the following case:
                #   // /* this is an inline comment */
                line += '*/'


        if '/*' in line and '*/' in line:
            # then a block documentation starts, but
            # it ends in the same line. For example:
            #   private /*final static */ String value = "foo";

            # the ' ' is to take into account the following cases:
            #       prublic/* static */Object foo;
            line = line[:line.index('/*')].rstrip() + ' ' + line[line.index('*/') + 2:].lstrip()
        elif '/*' in line:
            # in this case a comment block strarts here but doesn't
            # ends in the same line.
            line = line[:line.index('/*')].rstrip()
            tmp = line
            while '*/' not in tmp:
                position += 1
                tmp = content[position]

            line += tmp[tmp.index('*/') + 2:].lstrip()

        line = line.strip()
        if line:
            # the line might be empty if it was only a comment line.
            # For example:
            #       // this is a comment.
            res.append(line)

        position += 1
        if position == len(content):
            break

    return res


def remove_keywords(current_line, keywords):
    ''' Identifies which of the keywords can be in the current line and
    remove them.

    >>> remove_keywords('private static final int i = 3;', ['static', 'final'])
    'private int i = 3;'

    :parameters:
        current_line: str
            the current line of the file
        keywords: list(str)
            the keywords to remove of the line

    :returns:
        the line without the keywords.
    '''
    data = current_line.split(' ')
    data = map(lambda l: l.strip(), data)
    data = filter(lambda l: l.strip(), data)

    final = filter(lambda d: not d in keywords, data)
    return ' '.join(final)


def get_visibility(line):
    ''' Returns the visibility of the line.

    >>> get_visibility('private int i')
    'private'
    >>> get_visibility('int i')
    'protected'

    :returns:
        one of the valid visibility for the line, that
        must be a class definition, attribute or method.
    '''
    for visibility in VISIBILITY_VALUES:
        if has_any_keyword(line, [visibility]):
            return visibility

    if has_any_keyword(line, ['internal']):
        return 'private'

    # return the default visibility for the line
    return 'protected'


def get_type_and_name(current_line, index, class_model):
    ''' Return the variable type or the return class of the method.

    >>> get_type_and_name('int i', 0, current_class)
    ('int', i)
    >>> get_type_and_name('List<Foo> i', 0, current_class)
    ('List<Foo>', i)


    :parameters:
        current_line: str
            the complete definition attribute or method without any
            modifier.
        class_model: `pywebuml.models.Class`
            the current model that is being parsed. It will only
            be used to check if it is an enum


    :returns:
        a (str, str) str with the type of the variable, and the name of
        the attribute.
    '''
    is_enum = isinstance(class_model, Enum)

    # can't use current_line.split(' '), becuase there can be more than
    # one space between the type and variable definition
    if ' ' not in current_line and not is_enum:
        raise EmptyNameException(current_line, index)

    elif ' ' not in current_line and is_enum:
        variable_name = current_line.split(',', 1)[0]
        variable_name = variable_name.split(';', 1)[0]
        variable_name = variable_name.strip()
        return (class_model.package, variable_name)


    # TODO use the class_parser method to check if the current
    # line is a method or not.
    if is_enum and not '{' in current_line and '(' in current_line:
        variable_name = current_line.split('(', 1)[0]
        variable_name = variable_name.split(',', 1)[0]
        variable_name = variable_name.split(';', 1)[0]
        variable_name = variable_name.strip()
        return (class_model.package, variable_name)
    else:
        variable_type, name = current_line.rsplit(' ', 1)
        variable_type = variable_type.strip()

        if '>' in name:
            # take into account generics as:
            #   public List<Foo>mValues;
            variable_type += name[:name.rindex('>')+1]
            name = name[name.rindex('>')+1:]

        if '[]' in name:
            # take into account array definitions as:
            #   public int []mValues;
            variable_type += '[]'
            name = name.replace('[]', '')

        if ' ' in variable_type and not ('[]' in variable_type or '<' in variable_type):
            raise EmptyNameException(current_line, index)

        if ' ' in name or name == '':
            raise EmptyNameException(index, current_line)

        return (variable_type, name)
