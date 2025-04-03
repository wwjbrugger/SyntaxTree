import copy

from .abstract_operator import AbstractOperator
import numpy as np


class Power(AbstractOperator):
    def __init__(self, node):
        # child_1 is the power
        super().__init__(node)
        self.num_child = 2
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
            c_1_str = (self.node.list_children[1].math_class
                       .prefix_notation(self.node.node_id, kwargs))
            return f' ** {c_0_str} {c_1_str} '          #  p = c_0 ** c_1
        elif call_node_id == self.node.list_children[1].node_id:
            p_str = self.node.parent_node.math_class.prefix_notation(
                self.node.node_id, kwargs)
            c_0_str = (self.node.list_children[0].math_class
                       .prefix_notation(self.node.node_id, kwargs))
            return f' / log {p_str} log {c_0_str} '
            # c_1 = log_c_0( p)
            # log_c_0(p) = log_10(p) / log_10(c_0)

        elif call_node_id == self.node.list_children[0].node_id:
            p_str = self.node.parent_node.math_class.prefix_notation(
                self.node.node_id, kwargs)
            c_1_str = (self.node.list_children[1]
                       .math_class.prefix_notation(self.node.node_id, kwargs))
            return f' **  {p_str} / 1 {c_1_str}'

    def infix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            p_str = self.node.parent_node.math_class.infix_notation(call_node_id=self.node.node_id, kwargs=kwargs)
            return p_str
        elif call_node_id == self.node.parent_node.node_id or call_node_id is None:
            c_0_str = self.node.list_children[0].math_class.infix_notation(self.node.node_id, kwargs)
            c_1_str = self.node.list_children[1].math_class.infix_notation(self.node.node_id, kwargs)
            return f'  {c_0_str}  **' \
                   f'  {c_1_str}  '
        elif call_node_id == self.node.list_children[1].node_id:
            p_str = self.node.parent_node.math_class.infix_notation(call_node_id=self.node.node_id, kwargs=kwargs)
            c_0_str = self.node.list_children[0].math_class.infix_notation(self.node.node_id, kwargs)
            return f' log ( {p_str} ) / ' \
                   f' log ( {c_0_str} ) '
        elif call_node_id == self.node.list_children[0].node_id:
            p_str = self.node.parent_node.math_class.infix_notation(call_node_id=self.node.node_id, kwargs=kwargs)
            c_1_str = self.node.list_children[1].math_class.infix_notation(self.node.node_id, kwargs)
            return f'  {p_str}  ** ( 1 / {c_1_str} ) '

    def residual(self, call_node_id, dataset, kwargs):
        if call_node_id == self.node.list_children[1].node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            c_0 = self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
            return np.divide(np.log(p, dtype=np.float64), np.log(c_0, dtype=np.float64),dtype=np.float64)
        elif call_node_id == self.node.list_children[0].node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            c_1 = self.node.list_children[1].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
            return np.power(p, np.divide(1, c_1, dtype=np.float64), dtype=np.float64)
        elif call_node_id == self.node.node_id:
            p = self.node.parent_node.math_class.residual(self.node.node_id, dataset, kwargs)
            return p

    def evaluate_subtree(self, call_node_id, dataset, kwargs):
        child_0 = self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
        child_1 = self.node.list_children[1].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)
        return np.power(child_0,child_1 , dtype=np.float64)

    def delete(self):
        pass

    def __str__(self):
        return '**'

    def propagate_units(self, call_node_id, kwargs, dataset, changed=False):
        changed = propagate_units_power(self.node, call_node_id, kwargs, dataset, changed)
        return changed

def propagate_units_power(node, call_node_id, kwargs, dataset, changed=False):
    units_self = copy.copy(node.units.units)
    units_c0 = copy.copy(node.list_children[0].units.units)
    units_c1 = copy.copy(node.list_children[1].units.units)
    exponent = node.list_children[1].math_class.evaluate_subtree(
            call_node_id=node.node_id,
            dataset=dataset,
            kwargs=kwargs)[0]
    if exponent == 0.:
        changed |= node.units.update([0. for i in range(node.tree.args.unit_dimension)])
    else:
        changed |= node.units.update(
            [u * exponent if isinstance(u, float) else f"{u} * {exponent}"
             for u in units_c0]
        )
        #     #  {p_str}  ** ( 1 / {c_1_str} )
        changed |= node.list_children[0].units.update(
            [u / exponent if isinstance(u, float) else f"{u} / {exponent}"
             for u in units_self]
        )
    #  c1 =  log ( {p_str} ) /  log ( {c_0_str} )
    changed |= node.list_children[1].units.update([0. for i in range(node.tree.args.unit_dimension)]    )


    if call_node_id == node.node_id or call_node_id is None:
        changed |= node.parent_node.math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        changed |= node.list_children[0].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        changed |= node.list_children[1].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
    elif call_node_id == node.parent_node.node_id:
        changed |= node.list_children[0].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        changed |= node.list_children[1].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
    elif call_node_id == node.list_children[0].node_id:
        changed |= node.parent_node.math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        changed |= node.list_children[1].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
    elif call_node_id == node.list_children[1].node_id:
        changed |= node.parent_node.math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        changed |= node.list_children[0].math_class.propagate_units(call_node_id=node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
    return changed


