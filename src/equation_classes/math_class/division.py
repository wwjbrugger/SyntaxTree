import copy

import numpy as np
from src.equation_classes.math_class.abstract_operator import AbstractOperator
from src.equation_classes.math_class.multiplication import calculate_units


class Division(AbstractOperator):
    def __init__(self, node):
        super().__init__(node)
        self.num_child = 2
        self.node = node
        self.neutral_element = 1
        self.invertible = True

    def prefix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            return self.node.parent_node.math_class.prefix_notation(
                call_node_id=self.node.node_id, kwargs=kwargs)

        elif call_node_id == self.node.parent_node.node_id or call_node_id is None:
            return f""" / {self.node.list_children[0].math_class
            .prefix_notation(self.node.node_id, kwargs)} {self.node.list_children[1].math_class
            .prefix_notation(self.node.node_id, kwargs)} """

        elif call_node_id == self.node.list_children[0].node_id:
            return f""" * {self.node.parent_node.math_class
            .prefix_notation(self.node.node_id, kwargs)} {self.node.list_children[1].math_class
            .prefix_notation(self.node.node_id, kwargs)} """

        elif call_node_id == self.node.list_children[1].node_id:
            return f""" / {self.node.list_children[0].math_class
            .prefix_notation(self.node.node_id, kwargs)} {self.node.parent_node.math_class
            .prefix_notation(self.node.node_id, kwargs)}"""

    def infix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            return (self.node.parent_node.math_class.
                    infix_notation(self.node.node_id, kwargs))

        elif call_node_id == self.node.parent_node.node_id or call_node_id is None:
            return f"""( {self.node.list_children[0].math_class
            .infix_notation(self.node.node_id, kwargs)} / {self.node.list_children[1].math_class
            .infix_notation(self.node.node_id, kwargs)} ) """

        elif call_node_id == self.node.list_children[0].node_id:
            return f"""( {self.node.parent_node.math_class
            .infix_notation(self.node.node_id, kwargs)} * {self.node.list_children[1].math_class
            .infix_notation(self.node.node_id, kwargs)} ) """

        elif call_node_id == self.node.list_children[1].node_id:
            return f'( {self.node.list_children[0].math_class.infix_notation(self.node.node_id, kwargs)} /' \
                   f' {self.node.parent_node.math_class.infix_notation(self.node.node_id, kwargs)} ) '

    def residual(self, call_node_id, dataset, kwargs):
        if call_node_id == self.node.list_children[0].node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            c_1 = self.node.list_children[1].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
            return np.multiply(p, c_1, dtype=np.float64)
        elif call_node_id == self.node.list_children[1].node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            c_0 = self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
            return np.divide(c_0, p, dtype=np.float64)
        elif call_node_id == self.node.node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            return p

    def evaluate_subtree(self, call_node_id, dataset, kwargs):
        c_0 = self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
        c_1 = self.node.list_children[1].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
        return np.divide(c_0, c_1)

    def delete(self):
        pass

    def __str__(self):
        return '/'

    def propagate_units(self, call_node_id, dataset, kwargs, changed=False):

        units_self = copy.copy(self.node.units.units)
        units_c0 =  copy.copy(self.node.list_children[0].units.units)
        units_c1 =  copy.copy(self.node.list_children[1].units.units)
        # plus node get updates from adjacent nodes
        changed |= self.node.units.update(
            calculate_units(
                units_c0, units_c1,
                '-'
            )
        )
        changed |= self.node.list_children[0].units.update(
            calculate_units(
                units_self, units_c1,
                '+'
            )
        )
        changed |= self.node.list_children[1].units.update(
            calculate_units(
                units_c0, units_self,
                '-'
            )
        )

        if call_node_id == self.node.node_id or call_node_id is None:
            changed |= self.node.parent_node.math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
            changed |= self.node.list_children[0].math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
            changed |= self.node.list_children[1].math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        elif call_node_id == self.node.parent_node.node_id:
            changed |= self.node.list_children[0].math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
            changed |= self.node.list_children[1].math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        elif call_node_id == self.node.list_children[0].node_id:
            changed |= self.node.parent_node.math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
            changed |= self.node.list_children[1].math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        elif call_node_id == self.node.list_children[1].node_id:
            changed |= self.node.parent_node.math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
            changed |= self.node.list_children[0].math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        return changed
