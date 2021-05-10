from enum import Enum


class TreeNodeColor(Enum):
    red = 0
    black = 1


class TreeNode:
    left: 'TreeNode' = None
    right: 'TreeNode' = None
    parent: 'TreeNode' = None
    key: int
    value: int
    color: TreeNodeColor

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right


count = 0


def insert_into_tree(current_node: TreeNode, key: int, value: int) -> TreeNode:
    global count
    if current_node == None:
        current_node = TreeNode()
        current_node.key = key
        current_node.value = value
        current_node.color = TreeNodeColor.red if count > 0 else TreeNodeColor.black
        count += 1
        return current_node

    if current_node.key < key:
        current_node.right = insert_into_tree(
            current_node.get_right(), key, value)
        current_node.right.parent = current_node

    if current_node.key > key:
        current_node.left = insert_into_tree(
            current_node.get_left(), key, value)
        current_node.left.parent = current_node

    if current_node.color == TreeNodeColor.red:
        current_node.color = TreeNodeColor.black

        #right_blacks = count_blacks(current_node.right)
        #left_blacks = count_blacks(current_node.left)
        # if left_blacks - right_blacks < -1:

        # if right_blacks - left_blacks < -1:

    return current_node


def rotate_right(pivot: TreeNode):
    root = pivot.parent
    root.left = pivot.right
    pivot.right = root
    pivot.parent = root.parent
    if root.parent.left == root:
        root.parent.left = pivot
    elif root.parent.right == root:
        root.parent.right = pivot
    root.parent = pivot


def rotate_left(pivot: TreeNode):
    root = pivot.parent
    root.right = pivot.left
    pivot.left = root
    pivot.parent = root.parent
    if root.parent.left == root:
        root.parent.left = pivot
    elif root.parent.right == root:
        root.parent.right = pivot
    root.parent = pivot


def count_blacks(current_node: TreeNode) -> int:
    black_count = 0
    if current_node == None:
        return 0

    black_count += count_blacks(current_node.get_left())
    black_count += 1 if current_node.color == TreeNodeColor.black else 0
    black_count += count_blacks(current_node.get_right())
    return black_count


def print_inorder(current_node: TreeNode, test):
    if current_node == None:
        return

    print_inorder(current_node.get_left(), test + "-")
    print(test, current_node.key,
          current_node.parent.key if current_node.parent is not None else -1, current_node.color)
    print_inorder(current_node.get_right(), test + "-")


root = None
root = insert_into_tree(root, 35, 1)
root = insert_into_tree(root, 9, 1)
root = insert_into_tree(root, 50, 1)
root = insert_into_tree(root, 57, 1)
root = insert_into_tree(root, 68, 1)
#root = insert_into_tree(root, 43, 1)
#root = insert_into_tree(root, 46, 1)


# print_inorder(root, "")
# print()
# print("asdfgsadgfsadfasdfsadfasdfasddfsadfasdfasdfasfdasdf")
# print()
# rotate_left(root.right.right)

print(count_blacks(root))

print_inorder(root, "")
