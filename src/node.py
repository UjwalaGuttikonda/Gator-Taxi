class Node:

  def __init__(self, rn, rc, td):
    """
    Initialize a new node with the given parameters.

    rn: The node's RN (registration number).
    rc: The node's RC (record count).
    td: The node's TD (tree depth).
    """
    self.rn = rn
    self.rc = rc
    self.td = td
    self.parent = None  # Parent node.
    self.color = 1  # 1 for red, 0 for black.
    self.left = None  # Left child node.
    self.right = None  # Right child node.
    self.mpointer = None  # Pointer to a node in another tree.

  def print_color(self):
    """
    Returns a string representing the node's color.
    """
    if self.color == 0:
        return '(b)'  # Black node.
    return '(r)'  # Red node.

