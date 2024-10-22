
def print_tree(node, white_space=0):
    print(" " * white_space, node)
    for child in node.children:
        print_tree(child, white_space + 2)
