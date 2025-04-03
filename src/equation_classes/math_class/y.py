from .abstract_operator import AbstractOperator
import numpy as np

from .plus import use_more_concrete_units


class Y(AbstractOperator):
    def __init__(self, node):
        super().__init__(node)
        self.num_child = 1
        self.node = node
        self.invertible = True
        if hasattr(self.node.tree.args,'unit_dict'):
            if node.node_symbol in node.tree.args.unit_dict:
                self.node.units.units = node.tree.args.unit_dict[node.node_symbol]

    def prefix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            return self.node.list_children[0].math_class.prefix_notation(
                call_node_id=self.node.node_id, kwargs=kwargs)
        else:
            return f"{self.node.node_symbol}"

    def infix_notation(self, call_node_id, kwargs):
        if call_node_id == self.node.node_id:
            return self.node.list_children[0].math_class.infix_notation(call_node_id=self.node.node_id, kwargs=kwargs)
        else:
            return f" ( {self.node.node_symbol} ) "

    def residual(self, call_node_id, dataset, kwargs):
        return dataset.loc[:, self.node.node_symbol].to_numpy(dtype=np.float64)

    def evaluate_subtree(self, call_node_id, dataset, kwargs):
        return self.node.list_children[0].math_class.evaluate_subtree(self.node.node_id, dataset, kwargs)

    def delete(self):
        pass

    def propagate_units(self, call_node_id, kwargs, dataset, changed=False):
        changed |= self.node.units.update(use_more_concrete_units(
            self.node.tree.args,
            self.node.units.units, self.node.list_children[0].units.units,
            '=='
        )
        )
        changed |= self.node.list_children[0].units.update(use_more_concrete_units(
            self.node.tree.args,
            self.node.units.units, self.node.list_children[0].units.units,
            '=='
        )
        )
        if call_node_id == self.node.node_id or call_node_id is None:
            changed |= self.node.list_children[0].math_class.propagate_units(call_node_id=self.node.node_id, dataset=dataset, kwargs=kwargs, changed=changed)
        else:
            pass # We reached a leaf node the updates are handled by the operator nodes
        return changed

    def __str__(self):
        return 'y'
