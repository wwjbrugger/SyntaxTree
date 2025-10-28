from bisect import bisect_left


class MaxList:
    def __init__(self, args):
        self.max_elements_in_list = 10
        self.max_list_keys = []  # smallest element is right
        self.max_list_state = []
        self.complexity_dict = {}
        self.args = args

    def add(self, state, key, complexity=True):
        add(self.max_list_keys,
            self.max_list_state,
            state,
            key,
            self.max_elements_in_list)
        if complexity:
            nom_op = state.syntax_tree.num_inner_nodes()
            if nom_op not in self.complexity_dict:
                self.complexity_dict[nom_op] = MaxList(self.args)
                self.complexity_dict[nom_op].add(
                    state, key, complexity=False
                )
            else:
                self.complexity_dict[nom_op].add(
                    state, key, complexity=False
                )

    def __str__(self):
        return self.max_list_keys.__str__()


def add(max_list_keys, max_list_state, state, key, max_elements_in_list):
    if len(max_list_keys) >= max_elements_in_list:
        if max_list_keys[0] >= key:
            return
        else:
            max_list_keys.pop(0)
            max_list_state.pop(0)

    index = bisect_left(a=max_list_keys, x=key)
    max_list_keys.insert(index, key)
    max_list_state.insert(index, state)
