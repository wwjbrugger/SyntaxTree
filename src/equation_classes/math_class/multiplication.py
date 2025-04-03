import copy

import numpy as np
from .abstract_operator import AbstractOperator


class Multiplication(AbstractOperator):
    def __init__(self, node):
        super().__init__(node)
        self.num_child = 2
        self.node = node
        self.invertible = True
        self.neutral_element = 1

    def prefix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            return self.node.parent_node.math_class.prefix_notation(
                call_node_id=self.node.node_id, kwargs=kwargs)
        elif call_node_id == self.node.parent_node.node_id or call_node_id is None:
            return f' * {self.node.list_children[0].math_class.prefix_notation(self.node.node_id, kwargs)}' \
                   f' {self.node.list_children[1].math_class.prefix_notation(self.node.node_id, kwargs)} '
        elif call_node_id == self.node.list_children[0].node_id:
            return f' / {self.node.parent_node.math_class.prefix_notation(self.node.node_id, kwargs)}' \
                   f' {self.node.list_children[1].math_class.prefix_notation(self.node.node_id, kwargs)} '
        elif call_node_id == self.node.list_children[1].node_id:
            return f' / {self.node.parent_node.math_class.prefix_notation(self.node.node_id, kwargs)}' \
                   f' {self.node.list_children[0].math_class.prefix_notation(self.node.node_id, kwargs)} '

    def infix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            return self.node.parent_node.math_class.infix_notation(call_node_id=self.node.node_id, kwargs=kwargs)
        elif call_node_id == self.node.parent_node.node_id or call_node_id is None:
            return f'( {self.node.list_children[0].math_class.infix_notation(self.node.node_id, kwargs)} *' \
                   f' {self.node.list_children[1].math_class.infix_notation(self.node.node_id, kwargs)} ) '
        elif call_node_id == self.node.list_children[0].node_id:
            return f'( {self.node.parent_node.math_class.infix_notation(self.node.node_id, kwargs)} /' \
                   f' {self.node.list_children[1].math_class.infix_notation(self.node.node_id, kwargs)} ) '
        elif call_node_id == self.node.list_children[1].node_id:
            return f'( {self.node.parent_node.math_class.infix_notation(self.node.node_id, kwargs)} /' \
                   f' {self.node.list_children[0].math_class.infix_notation(self.node.node_id, kwargs)} ) '

    def residual(self, call_node_id, dataset, kwargs):
        if call_node_id == self.node.list_children[0].node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            c_1 = self.node.list_children[1].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
            return np.divide(p, c_1, dtype=np.float64)
        elif call_node_id == self.node.list_children[1].node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            c_0 = self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
            return np.divide(p, c_0, dtype=np.float64)
        elif call_node_id == self.node.node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            return p

    def evaluate_subtree(self, call_node_id, dataset, kwargs):
        c_0 = self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
        c_1 = self.node.list_children[1].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
        return np.multiply(c_0, c_1, dtype=np.float64)

    def delete(self):
        pass

    def __str__(self):
        return '*'

    def canonical_form(self, changed):
        c_0 = self.node.list_children[0]
        c_1 = self.node.list_children[1]
        self.node.test_swap_two_child_nodes(c_0, c_1)

    def propagate_units(self, call_node_id,dataset, kwargs, changed=False):

        units_self = copy.copy(self.node.units.units)
        units_c0 =  copy.copy(self.node.list_children[0].units.units)
        units_c1 =  copy.copy(self.node.list_children[1].units.units)
        # plus node get updates from adjacent nodes
        changed |= self.node.units.update(
            calculate_units(
                units_c0, units_c1,
                '+'
            )
        )
        changed |= self.node.list_children[0].units.update(
            calculate_units(
                units_self, units_c1,
                '-'
            )
        )
        changed |= self.node.list_children[1].units.update(
            calculate_units(
                units_self, units_c0,
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

def calculate_units(units_0, units_1, str_operator):
    if str_operator == '+':
        f = np.add
    if str_operator == '-':
        f = np.subtract
    if str_operator == '*':
        f = np.multiply
    if str_operator == '/':
        f = np.divide

    result_unit = []
    for i, _ in enumerate(units_0):
        u_0 = units_0[i]
        u_1 = units_1[i]
        if isinstance(u_0, float) and isinstance(u_1, float):
            if u_1 == 0 and str_operator == '/':
                result_unit.append(0)
            else:
                result_unit.append(f(u_0, u_1))
        else:
            result_unit.append(f"( {u_0} ) {str_operator} ( {u_1} )")
    return result_unit
