# -*- coding: utf-8 -*-

'''
Defines de model classes and the connection to them
'''

from app import db



CLASS_TYPES = (
    'normal',
    'inner',
    'enum',
    'interface',
    'abstract',
)

# the visibility of a method or attribute of a class.
VISIBILITY_VALUES = (
    'public',
    'protected',
    'private'
)

PROGRAMMING_LANGUAGES = (
    "C#",
    "Java",
    "Python",
)

class Class(db.Model):
    ''' Represents the Java/C#/Python class.

    The values are:

    - discriminator: indicates if the class is normal or inner.

    - package: the complete path of the class. In the case of C#
      it will be the namespace and the name of the class. For java
      it will be the package and the name of the class.

    - name: the name of the class without taking into account the
      namespace/package.

    - file_path: the filesystem path where the file of the class is located.
      In java it will be the same as the package without the class name. In C#
      it will be the path where the file was found. It is relative to where
      the command was executed.

    - programming_language: indicates the programming language of the class.
      The programming language will be used later on the web to remove
      the getter/setters of the class.

    - owner_package: if the class is defined inside another class, then
      it is the package of the owner.
    '''

    __tablename__ = 'classes'

    discriminator = db.Column('type', db.String(50))
    package = db.Column(db.String(1024), primary_key = True)
    name = db.Column(db.String(255))
    filepath = db.Column(db.String(1024), nullable = False)
    programming_language = db.Column(db.String(20), nullable = False)
    owner_package = db.Column(db.String(1024),
                            db.ForeignKey('classes.package'), nullable = True)

    owner = db.relationship('Class', remote_side = package, backref='inner_classes')

    __mapper_args__ = {'polymorphic_on': discriminator,
                        'polymorphic_identity': 'normal'}

    def __init__(self, package, name,
                 filepath , programming_language, owner = None):
        self.package = package
        self.name = name
        self.filepath = filepath
        self.programming_language = programming_language
        self.owner = owner

    def __eq__(self, other):
        return self.package == other.package

    def __hash__(self):
        return hash(self.package)

    def __repr__(self):
        return '<Class("%s", "%s")>' % (self.package, self.name)


class Interface(Class):
    ''' These classes are the one that are defined as interfaces.

    For example:
    public interface Foo {
    }
    '''
    __tablename__ = 'interfaces'
    __mapper_args__ = {'polymorphic_identity': 'interfaces'}

    interface_package_name = db.Column(db.String(1024), db.ForeignKey('classes.package'), primary_key = True)

    def __init__(self, package, name,
                        filepath, programming_language, owner = None):
        super(Interface, self).__init__(package, name,
                        filepath, programming_language, owner)
        self.interface_package_name = package


class Abstract(Class):
    ''' These are the abstract classes.
    '''

    __tablename__ = 'abstract'
    __mapper_args__ = {'polymorphic_identity': 'abstract'}

    abstract_package_name = db.Column(db.String(1024), db.ForeignKey('classes.package'), primary_key = True)

    def __init__(self, package, name,
                        filepath, programming_language, owner = None):
        super(Abstract, self).__init__(package, name,
                        filepath, programming_language, owner)
        self.abstract_package_name = package


class Enum(Class):
    ''' These are special classes that represents the enums.
    '''

    __tablename__ = 'enums'
    __mapper_args__ = {'polymorphic_identity': 'enums'}

    enum_package_name = db.Column(db.String(1024), db.ForeignKey('classes.package'), primary_key = True)

    def __init__(self, package, name,
                        filepath, programming_language, owner = None):
        super(Enum, self).__init__(package, name,
                        filepath, programming_language, owner)
        self.enum_package_name = package



class ClassInheritence(db.Model):
    ''' Represent the inheritence relationshipt between two classes.

    For example, if class A extends class B and C, then in the database
    there will the following rows:
        A   B
        A   C

    In some languages (Java) a class can only extend one class, but in
    other languages (Python) there is no such limitation.
    '''

    __tablename__ = 'class_inheritence'

    class_package = db.Column(db.String(1024), db.ForeignKey('classes.package'), primary_key = True)
    base_class_package = db.Column(db.String(1024), primary_key = True)

    class_model = db.relationship(Class, backref=db.backref('base_classes'))

    def __init__(self, class_model, base_class_package):
        self.class_model = class_model
        self.base_class_package = base_class_package

    def __hash__(self):
        return hash(self.class_package) + hash(self.base_class_package)

    def __eq__(self, other):
        return self.class_package == other.class_package and \
                self.base_class_package == other.base_class_package



class ClassImplements(db.Model):
    ''' Relates a class with the interfaces it implements.

    For example if class A implements D and E, then in the database there
    will be the folling rows:
        A   D
        A   E

    There are some clases that doesn't have interface (Python), so there
    won't be no rows in this table.

    The values are:
        class_package: the package of the class that implements the interfaces.
        interface_class_package: the package of the interface.
    '''

    __tablename__ = 'class_implementations'

    class_package = db.Column(db.String(1024), db.ForeignKey('classes.package'), primary_key = True)
    interface_class_package = db.Column(db.String(1024), primary_key = True)

    class_model = db.relationship(Class, backref=db.backref('implemented_interfaces'))

    def __init__(self, class_model, interface_class_package):
        self.class_model = class_model
        self.interface_class_package = interface_class_package

    def __hash__(self):
        return hash(self.class_package) + hash(self.interface_class_package)

    def __eq__(self, other):
        return self.class_package == other.class_package and \
                self.interface_class_package == other.interface_class_package



class Attribute(db.Model):
    ''' Represents each of the attributes of the class.

    It has the following fields:
    - The name is the name of the attribute,
    - the class_id is the class to which the attribute belongs,
    - the visibility indicates if it is private/protected/public
    - the type indicates the type of the attribute. It could be some
      basic system attribute (float, int, string, etc..) or a reference
      to another class. If it is a refernece, then the referenced_class_id
      will have the id of the ``Class``
    - is_final indicates if the value is const/final/etc..
    - is_static indicates if the attribute is static.
    '''

    __tablename__ = 'attributes'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    class_package = db.Column(db.String(1024), db.ForeignKey('classes.package'))
    visibility = db.Column(db.String(50))
    referenced_class_package = db.Column(db.Integer)
    is_final = db.Column(db.Boolean)
    is_static = db.Column(db.Boolean)

    class_model = db.relationship(Class, backref=db.backref('attributes'))

    def __init__(self, name, type, class_model, visibility,
                 is_static, is_final, referenced_class_package = None):
        self.name = name
        self.type = type
        self.class_model = class_model
        self.visibility = visibility
        self.is_final = is_final
        self.is_static = is_static
        self.referenced_class_package = referenced_class_package

    def __str__(self):
        return '<Attribute(%s)>' % self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.name) + hash(self.class_package)

    def __eq__(self, other):
        return self.name == other.name and \
                self.class_package == other.class_package

class Method(db.Model):
    ''' Represents a model of the class.

    It has the followin fields:
    - name: the name of the method
    - signature: the parameters and return class of the method. For example:
      sum(long a, long c) -> long
    - class_package: the package of the class that has this attribute.
    - visibility: indicates if it is private/protected/etc...
    - is_static: indicate if the method is static.
    - is_abstract: indicate if the method is abstract. If the class is
      an interface, then the method will be abstract
    '''

    __tablename__ = 'methods'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    class_package = db.Column(db.String(1024), db.ForeignKey('classes.package'))
    signature = db.Column(db.String(1024))
    visibility = db.Column(db.String(50))
    is_static = db.Column(db.Boolean)
    is_abstract = db.Column(db.Boolean)

    class_model = db.relationship(Class, backref=db.backref('methods'))


    def __init__(self, name, class_model, signature, visibility,
                is_static, is_abstract):
        self.name = name
        self.class_model = class_model
        self.signature = signature
        self.visibility = visibility
        self.is_static = is_static
        self.is_abstract = is_abstract

    def __str__(self):
        return '<Method("%s")>' % self.signature

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.signature) + hash(self.class_package)

    def __eq__(self, other):
        return self.signature == other.signature and \
                self.class_package == other.class_package

