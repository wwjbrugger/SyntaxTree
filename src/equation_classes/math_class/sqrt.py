import copy

from src.equation_classes.math_class.abstract_operator import AbstractOperator
import numpy as np


class Sqrt(AbstractOperator):
    def __init__(self, node):
        # child_1 is the power
        super().__init__(node)
        self.num_child = 1
        self.node = node
        self.invertible = True
        self.neutral_element = 1

    def prefix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            p_str = self.node.parent_node.math_class.prefix_notation(
                call_node_id=self.node.node_id,
                kwargs=kwargs)
            return p_str
        elif call_node_id == self.node.parent_node.node_id or call_node_id is None:
            c_0_str = (self.node.list_children[0].math_class
                       .prefix_notation(self.node.node_id, kwargs))
            return f' ** {c_0_str} 0.5 '          #  p = c_0 ** c_1
        elif call_node_id == self.node.list_children[0].node_id:
            p_str = self.node.parent_node.math_class.prefix_notation(
                self.node.node_id, kwargs)
            return f' **  {p_str} 2'

    def infix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            p_str = self.node.parent_node.math_class.infix_notation(call_node_id=self.node.node_id, kwargs=kwargs)
            return p_str
        elif call_node_id == self.node.parent_node.node_id or call_node_id is None:
            c_0_str = self.node.list_children[0].math_class.infix_notation(self.node.node_id, kwargs)
            return f' ( {c_0_str} )  ** 0.5 '
        elif call_node_id == self.node.list_children[1].node_id:
            p_str = self.node.parent_node.math_class.infix_notation(call_node_id=self.node.node_id, kwargs=kwargs)

            return f' ( {p_str} ) **    2'

    def residual(self, call_node_id, dataset, kwargs):
        if call_node_id == self.node.list_children[0].node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            return np.power(p, np.power(p, 2, dtype=np.float64), dtype=np.float64)
        elif call_node_id == self.node.node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            return p

    def evaluate_subtree(self, call_node_id, dataset, kwargs):
        child_0 = self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
        return np.sqrt(child_0, dtype=np.float64)

    def delete(self):
        pass

    def propagate_units(self, call_node_id, dataset, kwargs, changed=False):
        changed = propagate_units_sqrt(self.node, call_node_id,dataset, kwargs, changed)
        return changed

def propagate_units_sqrt(node, call_node_id,dataset, kwargs, changed=False):
    units_self = copy.copy(node.units.units)
    units_c0 = copy.copy(node.list_children[0].units.units)


    changed |= node.units.update(
        [0.5 * u if isinstance(u, float) else f"0.5 * {u}" for u in units_c0])
    changed |= node.list_children[0].units.update(
        [2 * u if isinstance(u, float) else f"2 * {u}" for u in units_self])


    if call_node_id == node.node_id or call_node_id is None:
        changed |= node.parent_node.math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        changed |= node.list_children[0].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
    elif call_node_id == node.parent_node.node_id:
        changed |= node.list_children[0].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
    elif call_node_id == node.list_children[0].node_id:
        changed |= node.parent_nod.math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
    return changed

