class AVLNode:
    def __init__(self, data):
        self.val = data
        self.Left = None
        self.Right = None
        self.height = 0

class AVLNodeTree:
    def __init__(self, data:int):
        self.root = AVLNode(data)
    
    def insert(self, data:int):
        self.root = self._insert(self.root,data)
    
    def _insert(self, node,data:int):
        if node == None:
            return AVLNode(data)
        elif node.val > data:
            node.Left = self._insert(node.Left, data)
        elif node.val <= data:
            node.Right = self._insert(node.Right, data)
        return self.balance_tree(node)


    def is_left_higher(self, node):
        return self.get_height(node.Left) > self.get_height(node.Right)

    def balance_tree(self, node):
        node.height = 1+ self._max(self.get_height(node.Left), self.get_height(node.Right))
        balance = self.get_balance(node)
        
        # left left
        if balance > 1 and self.is_left_higher(node.Left):
            print(f"left left  {node.val} ")
            node =  self._right_rotate(node)
            
        # left right
        elif balance > 1 and (not self.is_left_higher(node.Left)):
            print(f"left right  {node.Left.val} ")
            node.Left = self._left_rotate(node.Left)
            node =  self._right_rotate(node)
            
        # right left
        elif balance < -1 and self.is_left_higher(node.Right):
            print(f"right left  {node.Right.val} ")
            node.Right = self._right_rotate(node.Right)
            node =  self._left_rotate(node)
            
        # right right
        elif balance < -1 and (not self.is_left_higher(node.Right)):
            print(f"right right  {node.Right.val} ")
            node =  self._left_rotate(node)
            
        return node

    def _right_rotate(self,node):
        print(f"right rotate on {node.val}")
        left_child_node = node.Left
        if left_child_node is None:
            print(f" right rotate {node.val} {node.Left} ")
            print(self._inorder(self.root))
            if node.Right is not None:
                print(f" right rotate {node.val} {node.Right.val} ")
        left_child_node_right_child_node = left_child_node.Right
        left_child_node.Right = node
        node.Left = left_child_node_right_child_node
        node.height = 1+ self._max(self.get_height(node.Left), self.get_height(node.Right))
        left_child_node.height = 1+ self._max(self.get_height(left_child_node.Left), self.get_height(left_child_node.Right))
        
        return left_child_node

    def _left_rotate(self,node):
        print(f"left rotate on {node.val}")
        right_child_node = node.Right
        print(f"right child is {right_child_node.val}")
        right_child_node_left_child_node = right_child_node.Left
        if right_child_node_left_child_node is not None:
            print(f"right_child_node_left_child_node is {right_child_node_left_child_node.val}")
        right_child_node.Left = node
        print(f"right_child_node.Left is {right_child_node.Left.val}")
        node.Right = right_child_node_left_child_node
        if node.Right is not None:
            print(f"node.Right is {node.Right.val}")
        node.height = 1+ self._max(self.get_height(node.Left), self.get_height(node.Right))
        print(f"node.height is {node.height}")
        right_child_node.height = 1+ self._max(self.get_height(right_child_node.Left), self.get_height(right_child_node.Right))
        print(f"right_child_node.height is {right_child_node.height}")
        
        return right_child_node

    def get_height(self, node):
        if node == None:
            return -1
        else:
            return node.height

    def _max(self,a, b):
        if a > b:
            return a
        return b

    def get_balance(self, node):
        # node can not be None if called by get_balance
        # if node is None:
        #     return 0
        return self.get_height(node.Left) - self.get_height(node.Right)

    def find(self, data):
        return self._find(self.root, data)

    def _find(self, node, data):

        current = node
        while True:
            if current is None:
                print(f"not find data {data}")
                return None
            elif current.val > data:
                current = current.Left
            elif current.val < data:
                current = current.Right
            else:
                print(f" find data {data}")
                return data
            

    def inorder(self):
        return self._inorder(self.root)
    def _inorder(self, node):
        if node == None:
            return []
        
        return self._inorder(node.Left) + [node.val] + self._inorder(node.Right)
    def preorder(self):
        return self._preorder(self.root)
    def _preorder(self, node):
        if node == None:
            return []
        
        return [node.val] +self._preorder(node.Left) +  self._preorder(node.Right)
    def postorder(self):
        return self._postorder(self.root)
    def _postorder(self, node):
        if node == None:
            return []
        
        return self._postorder(node.Right)  +self._postorder(node.Left) +  [node.val]
    
    def delete(self, data):
        self.root = self._delete(self.root,data)
    def _delete(self, node, data):
        if node == None:
            print("could not find the data to delete")
            return None
        elif node.val > data:
            node.Left = self._delete(node.Left,data)
        elif node.val < data:
            node.Right = self._delete(node.Right,data)
        elif node.val == data:
            if node.Left == None and node.Right == None:
                return None
            elif node.Right:
                node.val = self._max_right(node.Right)
                node.Right = self._delete(node.Right, node.val)
                return node
            else:
                return node.Left
        return self.balance_tree(node)

    def _max_right(self, node):
        if node.Left == None:
            return node.val
        else:
            return self._max_right(node.Left)


t = AVLNodeTree(15)
arr = [88, 98, 42, 3, 34, 24, 64, 74, 85, 95, 30, 3, 66, 53, 41, 7, 84, 5, 13, 68]
# arr = []
# for i in range(20):
#     arr.append(random.randint(1,100))
# print(arr)
for i in arr:
    t.insert(i)

print("is the val 42 in the tree ", t.find(42))
print("is the val 22 in the tree ", t.find(22))

print("the inorder of the tree ",t.inorder())
print("the preorder of the tree ",t.preorder())
print("the postorder of the tree ",t.postorder())

t.delete(42)
print("the inorder of the tree ",t.inorder())
print("the preorder of the tree ",t.preorder())
print("the postorder of the tree ",t.postorder())
    
        