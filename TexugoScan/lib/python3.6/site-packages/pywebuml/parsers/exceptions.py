# -*- coding: utf-8 -*-

'''
Exceptions raised by the different parsers.
'''

class ParserException(Exception):
    pass


class BadClassDefinition(ParserException):
    ''' Used when the class definition is wrong.
    For example, a missing '}'
    '''
    pass


class MissingOpeningClassDefinition(ParserException):
    ''' Raised when the class definitios is missing it's '{'.

    For example:

    public class Foo
        private int bar = 4;
    };
    '''
    pass

class MissingClosingClassDefinition(ParserException):
    ''' Raised when the class is missing its closing '}'.

    For example:

    public class Foo {
        private int bar = 3;

    '''
    
    def __init__(self, index):
        self.index = index
        
    def __str__(self):
        return "Cant find closing '}' for class definition that started on line: %s" % self.index 

class BadMethodDefinition(ParserException):
    ''' Used when a method definition is wrong.
    '''
    pass

class MissingClosingParenthesis(BadMethodDefinition):
    ''' Used when a closing parenthesis is missing for the
    class definition.
    '''
    
    def __init__(self, line_number):
        ''' Initializer..
        
        :parameters:
            line_number: int
                the line number of the parsing file where the exception 
                was raised.
        '''
        self.line = line_number
        
    def __str__(self):
        return "Can't find closing ')'for method definition " + \
               "that started at line: %s" % self.line

class MissingClosingMethod(BadMethodDefinition):
    ''' Used when a closing '}' for the method is missing.
    '''
    
    def __init__(self, line_number):
        '''
        '''
        self.line = line_number
        
    def __str__(self):
        return "Can't find closing '}' for method that started at line: %s" % self.line


class BadAttributeDefinition(ParserException):
    ''' Used when it couldn't parse an atribute.
    '''
    pass

class ClossingArrayException(BadAttributeDefinition):
    ''' Error raised when the array closing } is missing.
    '''
    
    def __init__(self, line_number):        
        self.line = line_number
        
    def __str__(self):
        return "Can't find closing '}' for array definition that started at line: %s" % self.line
        
class EmptyNameException(BadAttributeDefinition):
    ''' Error raised when the attribute name  or method couldn't be fetched.
    
    For example, when the name of the attribute has an space,
    or when isn't defined. For example:
    
        private modifier1 modifier2 int[]
        private int = 3;
        
    where modifier1, modifier2 don't exist in the language definition.
    '''
    
    def __init__(self, line_number, name):        
        self.line = line_number
        self.name = name
        
    def __str__(self):
        return "Can't find property name for attribute defined in: %s. The name was: %s" % (self.line, self.name)

