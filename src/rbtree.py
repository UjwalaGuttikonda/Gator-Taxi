import node as node1

class RedBlackTree:

    def __init__(self):
        # Initialize the root node and a NIL node, which acts as the null/leaf node in the tree
        self.NIL = node1.Node(-1, -1, -1)  # arbitrary value
        self.NIL.color = 0
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL

    # Rotate the node to the left 
    def leftrotate(self, node):
        y = node.right
        node.right = y.left

        # Update the parent of the left child of y, if it exists
        if y.left != self.NIL:
            y.left.parent = node

        y.parent = node.parent

        if node.parent is None:
            # If node is the root node, update the root
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y

        y.left = node
        node.parent = y


    # Rotate the node to the right
    def rightrotate(self, node):
        y = node.left
        node.left = y.right

        # Update the parent of the right child of y, if it exists
        if y.right != self.NIL:
            y.right.parent = node

        y.parent = node.parent

        if node.parent is None:
            # If node is the root node, update the root
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y

        y.right = node
        node.parent = y

    # Insert a node with a ride number and a color
    def insert(self, rn, rc, td):
        # If a node with the ride number already exists, return an error message
        err = "Duplicate RideNumber"
        checknode = self.search(rn)
        if checknode != self.NIL: 
            return err
        
        # Create a new node and initialize its values
        newnode = node1.Node(rn, rc, td)
        newnode.left = self.NIL
        newnode.right = self.NIL

        y = None
        x = self.root

        # Traverse down the tree to find the position for the new node
        while x != self.NIL:
            y = x
            if newnode.rn < x.rn:
                x = x.left
            else:
                x = x.right

        newnode.parent = y
        if y == None:
            # If the tree is empty, set the new node as the root node
            self.root = newnode
        elif newnode.rn < y.rn:
            y.left = newnode
        else:
            y.right = newnode

        self.fixinsert(newnode)

  # O(logn) , Called to check if RBT Properties are satisfied or not. If not, then the tree is fixed with recoloring/rotation/both.
    def fixinsert(self, newnode):
      # loop until the node has parent and the parent color is red
      while newnode.parent and newnode.parent.color == 1:
        if newnode.parent == newnode.parent.parent.left:
          # if the parent is the left child of its parent
          y = newnode.parent.parent.right
          if y.color == 1:
            # if the right uncle node is red
            # color the parent and uncle node black and grandparent red
            newnode.parent.color = 0
            y.color = 0
            newnode.parent.parent.color = 1
            newnode = newnode.parent.parent
          else:
            if newnode == newnode.parent.right:
              # if the newnode is the right child of the parent
              # left rotate parent and the newnode to make the newnode the parent
              newnode = newnode.parent
              self.leftrotate(newnode)
            # color the parent and grandparent
            newnode.parent.color = 0
            newnode.parent.parent.color = 1
            # right rotate grandparent
            self.rightrotate(newnode.parent.parent)
        else:
          # if the parent is the right child of its parent
          y = newnode.parent.parent.left
          if y.color == 1:
            # if the left uncle node is red
            # color the parent and uncle node black and grandparent red
            newnode.parent.color = 0
            y.color = 0
            newnode.parent.parent.color = 1
            newnode = newnode.parent.parent
          else:
            if newnode == newnode.parent.left:
              # if the newnode is the left child of the parent
              # right rotate parent and the newnode to make the newnode the parent
              newnode = newnode.parent
              self.rightrotate(newnode)
            # color the parent and grandparent
            newnode.parent.color = 0
            newnode.parent.parent.color = 1
            # left rotate grandparent
            self.leftrotate(newnode.parent.parent)
        if newnode == self.root:
          break
      # color the root black
      self.root.color = 0
      
  # O(logn) total
    def delete(self, rn):
      node = self.search(rn)
      if node == self.NIL:
        return

      y = node
      y_ogcolor = y.color

      # case 1
      if node.left == self.NIL:
        x = node.right
        self.transplant(node, node.right)
      # case 2
      elif node.right == self.NIL:
        x = node.left
        self.transplant(node, node.left)
      # case 3
      else:
        y = self.minimum(node.right)
        y_ogcolor = y.color
        x = y.right

        if y.parent == node:
          x.parent = y
        else:
          self.transplant(y, y.right)
          y.right = node.right
          y.right.parent = y

        self.transplant(node, y)
        y.left = node.left
        y.left.parent = y
        y.color = node.color

      if y_ogcolor == 0:
        self.fixdelete(x)

  # O(logn)
    def fixdelete(self, x):
      while x != self.root and x.color == 0:
        if x == x.parent.left:
          v = x.parent.right
          # type 1
          if v.color == 1:
            v.color = 0
            x.parent.color = 1
            self.leftrotate(x.parent)
            v = x.parent.right
          # type 2
          if v.left.color == 0 and v.right.color == 0:
            v.color = 1
            x = x.parent
          else:
            # type 3
            if v.right.color == 0:
              v.left.color = 0
              v.color = 1
              self.rightrotate(v)
              v = x.parent.right
            # type 4
            v.color = x.parent.color
            x.parent.color = 0
            v.right.color = 0
            self.leftrotate(x.parent)
            x = self.root
        else:
          v = x.parent.left
          # type 1
          if v.color == 1:
            v.color = 0
            x.parent.color = 1
            self.rightrotate(x.parent)
            v = x.parent.left
          # type 2
          if v.right.color == 0 and v.left.color == 0:
            v.color = 1
            x = x.parent
          else:
            # type 3
            if v.left.color == 0:
              v.right.color = 0
              v.color = 1
              self.leftrotate(v)
              v = x.parent.left
            # type 4
            v.color = x.parent.color
            x.parent.color = 0
            v.left.color = 0
            self.rightrotate(x.parent)
            x = self.root
      x.color = 0

  # O(1)
    def transplant(self, u, v):
      if u.parent == None:
        self.root = v
      elif u == u.parent.left:
        u.parent.left = v
      else:
        u.parent.right = v
      v.parent = u.parent

  # O(h) = O(logn) for RB trees
    def minimum(self, x):
      while x.left != self.NIL:
        x = x.left
      return x

  # O(h) = O(logn) for RB trees
    def search(self, rnval):
      node = self.root
      while node != self.NIL and rnval != node.rn:
        if rnval < node.rn:
          node = node.left
        else:
          node = node.right
      return node

    def Print(self, rn1, rn2):
      arr = []
      self.printnodes(arr, self.root, rn1, rn2)
      return arr

    def printnodes(self, arr, node, rn1, rn2):
      if node != self.NIL:
        self.printnodes(arr, node.left, rn1, rn2)
        if node.rn >= rn1 and node.rn <= rn2:
          arr.append((node.rn, node.rc, node.td))
        self.printnodes(arr, node.right, rn1, rn2)

    def UpdateTrip(self, rn, newtd):
      node = self.search(rn)
      if newtd <= node.td:
        node.td = newtd
      elif node.td <= newtd <= 2 * node.td:
        temprc = node.rc
        self.delete(node.rn)
        self.insert(node.rn, temprc + 10, newtd)
      elif newtd > 2 * node.td:
        self.delete(node.rn)