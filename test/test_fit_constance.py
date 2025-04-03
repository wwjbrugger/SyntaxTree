import unittest
from src.syntax_tree.syntax_tree import SyntaxTree
import pandas as pd
import numpy as np

def get_empty_list(arg):
    return []


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
        self.args.max_len_datasets = 10
        self.args.max_elements_in_best_list = 10
        self.args.max_num_nodes_in_syntax_tree = 30

        self.args.precision = 'float32'

    def test_0(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='+ c x_2'.split())

        columns = ['x_4', 'x_3', 'x_0', 'x_2', 'x_1', 'y']
        dataset = np.array([
            [- 10.08902, - 10.17091, 0.215567, 0.144374, 10.0676, - 9.089025],
            [- 7.930019, - 9.765913, 1.442015, 0.152672, 8.89528, - 6.930019],
            [- 5.511989, - 9.767252, 2.458630, 0.353149, 7.76481, - 4.511989],
            [- 3.271325, - 9.527846, 3.300389, 0.583482, 6.78344, - 2.271325],
            [- 1.169702, - 9.483120, 4.553673, 0.426493, 5.84703, - 0.169702],
            [1.076235, - 9.438329, 5.722373, 0.766701, 4.58014, 2.076235],
        ])
        df = pd.DataFrame(data=dataset,
                          columns=columns
                          )
        syntax_tree.fit_constants(
            call_node_id=-1,
            dataset=df,
            mode='evaluate'
        )

        pass

    def test_1(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='+ c x_2'.split())

        columns = ['x_4', 'x_3', 'x_0', 'x_2', 'x_1', 'y']
        dataset = np.array([
            [- 10.08902, - 10.17091, 0.215567, 1, 10.0676, 1],
            [- 7.930019, - 9.765913, 1.442015, 2, 8.89528, 2],
            [- 5.511989, - 9.767252, 2.458630, 3, 7.76481, 3],
            [- 3.271325, - 9.527846, 3.300389, 4, 6.78344, 4],
            [- 1.169702, - 9.483120, 4.553673, 5, 5.84703, 5],
            [1.076235, - 9.438329, 5.722373, 6, 4.58014, 6],
        ])
        df = pd.DataFrame(data=dataset,
                          columns=columns
                          )
        syntax_tree.fit_constants(
            call_node_id=-1,
            dataset=df,
            mode='evaluate'
        )
        np.testing.assert_almost_equal(1,
                                       syntax_tree.constants_in_tree['c_0']['value'],
                                       decimal=1)

    def test_2(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)
        syntax_tree.prefix_to_syntax_tree(prefix='/ * + c x_0 - c x_1 c'.split())

        columns = ['x_0', 'x_1', 'x_2', 'x_3', 'x_4', 'y']
        dataset = np.array([
            [1, 5, 0.215567, 1, 10.0676, -5],
            [2, 7, 1.442015, 2, 8.89528, -14],
            [3, 2, 2.458630, 3, 7.76481, -6],
            [4, 3, 3.300389, 4, 6.78344, -12],
            [5, 4, 4.553673, 5, 5.84703, -20],
            [6, 5, 5.722373, 6, 4.58014, -30],
        ])
        df = pd.DataFrame(data=dataset,
                          columns=columns
                          )
        syntax_tree.fit_constants(
            call_node_id=-1,
            dataset=df,
            mode='evaluate'
        )

        np.testing.assert_almost_equal(0, syntax_tree.constants_in_tree['c_0']['value'],
                                       decimal=1)
        np.testing.assert_almost_equal(0, syntax_tree.constants_in_tree['c_1']['value'],
                                       decimal=1)

        np.testing.assert_almost_equal(1, syntax_tree.constants_in_tree['c_2']['value'],
                                       decimal=1)



