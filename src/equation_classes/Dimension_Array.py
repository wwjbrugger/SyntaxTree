"""
The idea of the class is that we have an array with 2 x units.
the array with index 0 shows the unit information from the parent node.
the array with index 1 shows the unit information from the child node.
An element in the array can be a float or a string.
The string is needed if the units of the adjacent node are not clear.
In this context we can write s.t. like string =  n_[node_id} op n_[node_id}
The method consistent checks if  array with index 0  and array with index 1 are equal if not false is returned
"""
import numpy as np


class UnitArray:
    def __init__(self, args, node):
        #self.parent_units = create_unit_array(args)
        self.units = create_unit_array(args)
        self.update_str = True # once we allow to upload the string conditions
        #self.child_units = create_unit_array(args)
        self.node=node

    # def consistent(self):
    #     return np.equal(self.parent_units, self.child_units)

    def __repr__(self):
        return f"UnitArray(parent_units={self.parent_units}, child_units={self.child_units})"

    def update(self,new_array):
        changed = False
        for i in range(len(new_array)):
            old = self.units[i]
            new = new_array[i]
            if isinstance(old, float) and isinstance(new, str):
                continue
            elif isinstance(old, str) and isinstance(new, float):
                self.units[i] = new
                changed = True
            elif isinstance(old, float) and isinstance(new, float):
                if not old == new:
                    raise UnitError(f"Error in calculating units:  {self.node.tree.__str__()}")
            elif isinstance(old, str) and isinstance(new, str):
                # do it only once
                if not new in old and self.update_str:
                    self.units[i] = f"{old} == {new} "
                    changed = True
        self.update_str = False
        return changed

    def __str__(self):
        return self.units.__str__()



def create_unit_array(args):
    return ['_' for i in range(args.unit_dimension)]




class UnitError(Exception):
    pass
