# -*- coding: utf-8 -*-

'''
Has a basic tree structure.

The tree won't be normal because it take into account that it
will represents the package of the ``pywebuml.model.Class``. For example:

org.
    apache
        foo
        bar
    android
        etc...
'''

class TreeNode(object):
    ''' Represents a node of the tree.
    '''
    
    def __init__(self, name, full_package):
        ''' Creates the tree node.
        
        :parameters:
            name: str
                the current piece of the package. It musn't
                have a '.', but it can be empty (only for the
                root node). For example:
                    A (see full_package)
				it chould also be the name of a class. For example,
				if the package is a class, then the value will be:
					Foo				
					
			full_package: str
				It could be a part of what is the full package of a class. It 
				represents the full_package until package. For example:
					global.A.C
					global.B.Foo
        '''
        self.full_package = full_package
        self.name = name
        self._childs = {}
        
    def add_child(self, left_package, checked_package=''):
        ''' Creates a child that has the package name.
        
		If the original left_package is: 'global.A.B.C.Foo', then
		the values will be:
			'global.A.B.C.Foo'	''
			'A.B.C.Foo'			'global'
			'B.C.Foo'			'C.Foo'
		
        :parameters:            
			left_package: str
				the part of the package that is left to create or find.								
			checked_package: str
				the checked part of the package.				
        '''
        name = self._split_package(left_package)
        parent_root = self._childs.get(name, False)
        checked_package = checked_package + '.' + name
        
        if not parent_root:
            parent_root = TreeNode(name, checked_package)
            self._childs[name] = parent_root
                    
        if left_package.count('.') > 0:
            rest_of_package = left_package.split('.', 1)[1]
            parent_root.add_child(rest_of_package, checked_package)                  
        
    def get(self, package_name, recursive = False):
        ''' Returns the child node that has that name.
        
        :parameters:
            package_name: str
                the current package name to look up. It musn't
                have a '.'. For example:
                    global
            recursive: bool
                if True, if there is a child that starts with that name,
                then it will search into the inner part, else it will
                search only the first level of childs.
                    
        :returns:
            None if no child exists with that name, else the TreeNode
            with the package.
        '''        
        current_name = self._split_package(package_name)
        node = self._childs.get(current_name)
        if recursive and node and package_name.count('.') > 0:            
            package_name = package_name.split('.', 1)[1]
            return node.get(package_name, recursive)
            
        return node
		
    @property
    def childs(self):
		''' Returns the child of the package_tree.
		
		It will first return all the packages that have childs, and
		then all the childs that are leaves. Both "pieces" of the list
		will be sorted by its name.
		
		:returns:
			a list of `pywebuml.package_tree.TreeNode`.
		'''
		leaves = []
		not_leaves = []
		for tree_node in self._childs.values():
			if tree_node._childs:
				not_leaves.append(tree_node)
			else:
				leaves.append(tree_node)
		
		not_leaves.sort()
		leaves.sort()
		return not_leaves + leaves
                  
        
    def _split_package(self, package_name):
        return package_name.split('.', 1)[0]
