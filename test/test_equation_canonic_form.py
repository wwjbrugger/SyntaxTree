import unittest

from src.syntax_tree.syntax_tree import SyntaxTree


class TestEvaluation(unittest.TestCase):
    def setUp(self) -> None:
        class Namespace():
            def __init__(self):
                pass

        self.args = Namespace()
        self.args.logging_level = 40
        self.args.max_branching_factor = 2
        self.args.max_depth_of_tree= 8
        self.args.max_num_nodes_in_syntax_tree = 30
        self.args.max_constants_in_tree = 5
    def test_0(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='+ x + x 4'.split())
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()
        syntax_tree.to_canonical_form()
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()

        self.assertEqual('+ + 4 x x'.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())

    def test_1(self):
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='+ x + 4 x'.split())
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()
        syntax_tree.to_canonical_form()
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()

        self.assertEqual('+ + 4 x x'.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())

    def test_2(self):
        print('Test 2')
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='* a + 4 x'.split())
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()
        print('______________________________')
        syntax_tree.to_canonical_form()
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()

        self.assertEqual('* + 4 x a'.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())

    def test_3(self):
        print('Test 3')
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='+ a * 4 x'.split())
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()
        print('______________________________')
        syntax_tree.to_canonical_form()
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()

        self.assertEqual('+ * 4 x a'.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())


    def test_4(self):
        print('Test 4')
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='+ * 8 4 * x a'.split())
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()
        print('______________________________')
        syntax_tree.to_canonical_form()
        syntax_tree.rearrange_equation_infix_notation(-1)
        syntax_tree.print()

        self.assertEqual('+ * 4 8 * a x'.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())

    def test_5(self):
        print('Test 5')
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='+  *  4 8 *  a  x'.split())
        syntax_tree.print()
        print('______________________________')
        syntax_tree.to_canonical_form()

        syntax_tree.print()

        self.assertEqual('+ * 4 8 * a x'.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())



    def test_6(self):
        print('Test 6')
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='* + / 1 rec  * 0.563862133628852 cos rec    ** 3 static_adv'.split())
        syntax_tree.print()
        print('______________________________')
        syntax_tree.to_canonical_form()

        syntax_tree.print()

        self.assertEqual(' *  ** 3 static_adv   +  * 0.563862133628852  cos rec   / 1 rec   '.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())
        
    def test_7(self):
        print('Test 6')
        syntax_tree = SyntaxTree(grammar=None, args=self.args)

        syntax_tree.prefix_to_syntax_tree(prefix='/ m / 0.38980228 + adv sin + cos m*  ** 2 rec'.split())
        syntax_tree.print()
        print('______________________________')
        syntax_tree.to_canonical_form()

        syntax_tree.print()

        self.assertEqual(' / m  / 0.38980228  + adv  sin  +  ** 2 rec   cos m*    '.split(), syntax_tree.rearrange_equation_prefix_notation(-1)[1].split())