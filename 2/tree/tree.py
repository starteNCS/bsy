from enum import Enum

class TreeNodeColor(Enum):
    red = 0
    black = 1

class TreeNode:
    left: 'TreeNode' = None
    right: 'TreeNode' = None
    key: int
    value: int
    color: TreeNodeColor

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

def insert_into_tree(current_node: TreeNode, key: int, value: int) -> TreeNode:
    if current_node == None:
        current_node = TreeNode()
        current_node.key = key
        current_node.value = value
        return current_node

    if current_node.key < key:
        current_node.right = insert_into_tree(current_node.get_right(), key, value)

    if current_node.key > key:
        current_node.left = insert_into_tree(current_node.get_left(), key, value)

    return current_node

def print_inorder(current_node: TreeNode):
    if current_node == None:
        return

    print_inorder(current_node.get_left())
    print(current_node.key)
    print_inorder(current_node.get_right())

root = None
root = insert_into_tree(root, 0, 1)
root = insert_into_tree(root, 2, 1)
root = insert_into_tree(root, 3, 1)
root = insert_into_tree(root, 5, 1)
root = insert_into_tree(root, 69, 1)

print_inorder(root)