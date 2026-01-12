import unittest

import pandas as pd

from ..syntax_tree.syntax_tree import SyntaxTree
import numpy as np


class Get_residual_of_equation(unittest.TestCase):
    def setUp(self) -> None:


        class Namespace():
            def __init__(self):
                pass

        self.args = Namespace()
        self.args.logging_level = 40
        self.args.max_branching_factor = 2
        self.args.max_depth_of_tree = 10
        self.args.max_constants_in_tree = 5
        self.args.num_rows_for_ed = 10
        self.args.max_elements_in_best_list = 10
        self.args.max_num_nodes_in_syntax_tree = 30
        self.args.unit_dimension = 3

        self.args.precision = 'float32'
        self.args.unit_dict = {
            'x_0' : np.array([2.,1.,0.]),
            'x_2': np.array([2., 1., 0.]),
            'y': np.array([2., 1., 0.])
        }

    def test_absolute(self):
        self.args.unit_dict = {
            'x_0' : np.array([0.,1.,0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([0., 1., 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix=' abs x_0 '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_cosine(self):
        self.args.unit_dict = {
            'x_0' : np.array([0.,1.,0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([4., 2., 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='* c cos + c c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()


    def test_division_(self):
        self.args.unit_dict = {
            'x_0' : np.array([0.,1.,0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([4., 2., 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='* / x_0 x_1 + c c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_exp(self):
        self.args.unit_dict = {
            'x_0' : np.array([0.,1.,0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([0., 0 , 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix=' exp c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_log(self):
        self.args.unit_dict = {
            'x_0' : np.array([0.,1.,0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([0., 0 , 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix=' log c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_ln(self):
        self.args.unit_dict = {
            'x_0' : np.array([0.,1.,0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([0., 0 , 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix=' ln c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_minus(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='- x_0 - c x_2'.split())
        syntax_tree.start_node.parent_node.print()

        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_multiplication(self):
        self.args.unit_dict = {
            'x_0': np.array([2., 1., 0.]),
            'x_2': np.array([2., 1., 0.]),
            'y': np.array([4., 2., 0.])
        }

        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='* x_0  c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_plus(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)


        syntax_tree.prefix_to_syntax_tree(prefix='+ x_0 + c x_2'.split())
        syntax_tree.start_node.parent_node.print()

        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_plus_2(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)


        syntax_tree.prefix_to_syntax_tree(prefix='+ c + c c'.split())
        syntax_tree.start_node.parent_node.print()

        changed = True
        while changed:
            changed = syntax_tree.start_node.parent_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_power(self):
        self.args.unit_dict = {
            'x_0': np.array([2., 1., 0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([4., 2, 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)


        syntax_tree.prefix_to_syntax_tree(prefix='** x_0  2'.split())
        syntax_tree.start_node.parent_node.print()

        changed = True
        while changed:
            changed = syntax_tree.start_node.parent_node.math_class.propagate_units(
                call_node_id=None,
                kwargs=self.args.unit_dict,
                dataset=pd.DataFrame({'x_0':[0], 'x_1':[0], 'y':[0]}))
            print()
            syntax_tree.start_node.parent_node.print()

    def test_sine(self):
        self.args.unit_dict = {
            'x_0' : np.array([0.,1.,0.]),
            'x_1': np.array([2., 1., 0.]),
            'y': np.array([4., 2., 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='* c sin + c c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_sqrt(self):
        self.args.unit_dict = {
            'x_0': np.array([0., 1., 0.]),
            'x_1': np.array([8., 4., 0.]),
            'y': np.array([4., 2., 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='sqrt x_1 '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()

    def test_tan(self):
        self.args.unit_dict = {
            'x_0': np.array([0., 1., 0.]),
            'x_1': np.array([8., 4., 0.]),
            'y': np.array([0., 0., 0.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='tan c '.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(call_node_id=None, kwargs=self.args.unit_dict, dataset=None)
            print()
            syntax_tree.start_node.parent_node.print()



    def test_all(self):
        self.args.unit_dict = {
            'x_0' : np.array([1.,1.,6.]),
            'x_1': np.array([-1., 0., 2.]),
            'y': np.array([2., 1., 4.])
        }
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='/ + * sin c x_0 - x_0 x_0 x_2'.split())
        syntax_tree.start_node.parent_node.print()
        changed = True
        while changed:
            changed = syntax_tree.start_node.math_class.propagate_units(
                call_node_id=None,
                kwargs=self.args.unit_dict,
                dataset=None
            )
            print()
            syntax_tree.start_node.parent_node.print()









