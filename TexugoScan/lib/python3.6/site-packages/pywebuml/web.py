# -*- coding: utf-8 -*-

'''
The web part of the application
'''

import os
import uuid
from json import dumps

from flask import render_template
from flask import request
from pywebuml.app import app, db
from pywebuml.filters import create_edge, get_class_type, should_create_edge
from pywebuml.models import Class
from pywebuml.package_tree import TreeNode

all_classes = None
tree = None

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/child", methods=["GET"])
def get_tree_child():
    ''' Searches for the child packages of the selected package.
    '''
    parent = request.args.get('package')
    childs = tree.get(parent, False)
    return childs


@app.route("/autocomplete", methods=["GET"])
def autocomplete_search():
    ''' Search for the posible name of the classes.

    :parameters:
        term: str
            the term tby which the user is selecting
            the class. It an GET parameter under the key get.

    :returns:
        a list with the name of the classes.
    '''
    term = request.args.get('term')
    query = db.session.query(Class)
    query = query.filter(Class.name.like('%s%%' % term))
    return dumps([{'label' : klass.package } for klass in query.all()])


@app.route("/search", methods=['GET'])
def search():
    ''' Searches for the classes that should be shown in the graph.

    :paramters:
        selected_package: str
            the package of the main class to shown.
        levels: str
            the number of related class to show.
    '''
    package = request.args.get('selected_package')
    number_of_levels = int(request.args.get('levels', '3'))
    should_show_attributes = True if request.args.get('show_attributes') == 'true' else False
    should_show_methods = True if request.args.get('show_methods') == 'true' else False

    current_packages_names = set([package])
    searched_packages = set()
    res = set()

    for i in range(0, number_of_levels):
        query = Class.query.options(db.joinedload(Class.attributes,
                                                    Class.methods,
                                                    Class.inner_classes,
                                                    Class.base_classes,
                                                    Class.implemented_interfaces
                                                    ))
        query = query.filter(Class.package.in_(current_packages_names))
        classes = query.all()

        if not classes:
            # the query didn't bring any result so no new data
            # is required.
            break

        current_packages_names = set()
        for klass in classes:
            res.add(klass)
            searched_packages.add(klass.package)

            for attr in klass.attributes:
                if attr.referenced_class_package:
                    current_packages_names.add(attr.referenced_class_package)

            for inner in klass.inner_classes:
                if not inner.package in searched_packages:
                    current_packages_names.add(inner.package)

            for base in klass.base_classes:
                package = base.base_class_package
                if package not in searched_packages:
                    current_packages_names.add(package)

            for interface in klass.implemented_interfaces:
                package = interface.interface_class_package
                if package not in searched_packages:
                    current_packages_names.add(package)


        if not current_packages_names:
            # all the necesary packages are already fetched.
            break


    res = list(res)
    res.sort(key = lambda klass : klass.name)
    class_packages = [klass.package for klass in res]
    final_dot_info = render_template('classes.dot',
                            classes = res,
                            class_packages = class_packages,
                            should_show_methods = should_show_methods,
                            should_show_attributes = should_show_attributes,
                            )

    tmp_filename = _get_tmp_file()
    with open(tmp_filename + '.dot', 'w') as dot_file:
        dot_file.write(final_dot_info)

    # TODO check that this command didn't finish with any error
    os.system('dot -Tpng %s.dot -o %s.png' % (tmp_filename, tmp_filename))
    image_name = os.path.basename(tmp_filename)
    return render_template("index.html", image=image_name)


def _get_tmp_file():
    ''' Retuns the name of the dot file and the image file.
    Both files will be returned without any extension.
    Returns a path inside a temp folder so files can be easily deleted.

    :returns:
        the name of the dot an image file that shoudl be used without
        any extension
    '''
    return os.path.join(CURRENT_PATH, 'static', 'tmp_dir', str(uuid.uuid4()))


@app.context_processor
def inject_context():
    ''' Inject into the context all the classes, and the tree strutcture.
    '''
    return dict(all_classes=all_classes, tree=tree)


def start_app():
    ''' Starts the webapp.
    '''
    tmpdir_path = os.path.join(CURRENT_PATH, 'static', 'tmp_dir')
    if not os.path.exists(tmpdir_path):
        os.mkdir(tmpdir_path)

    all_classes = db.session.query(Class).order_by(Class.package).all()
    tree = TreeNode('', '')
    for klass in all_classes:
        tree.add_child(klass.package)
    app.jinja_env.filters['create_edge'] = create_edge
    app.jinja_env.filters['get_class_type'] = get_class_type
    app.jinja_env.filters['should_create_edge'] = should_create_edge
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    start_app()
