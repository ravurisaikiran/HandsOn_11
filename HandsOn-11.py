class Node:
    def __init__(self, key, color=None):
        self.key, self.left, self.right, self.parent = key, None, None, None
        self.height = 1
        self.color = color

class BinarySearchTree:
    def __init__(self): self.root = None

    def insert_node(self, key):
        def _insert(n, k):
            if not n: return Node(k)
            if k < n.key: n.left = _insert(n.left, k)
            elif k > n.key: n.right = _insert(n.right, k)
            return n
        self.root = _insert(self.root, key)

    def search_node(self, key):
        def _search(n, k):
            if not n or n.key == k: return n
            return _search(n.left, k) if k < n.key else _search(n.right, k)
        return _search(self.root, key)

    def delete_node(self, key):
        def _min(n):
            while n.left: n = n.left
            return n
        def _delete(n, k):
            if not n: return n
            if k < n.key: n.left = _delete(n.left, k)
            elif k > n.key: n.right = _delete(n.right, k)
            else:
                if not n.left: return n.right
                if not n.right: return n.left
                t = _min(n.right)
                n.key = t.key
                n.right = _delete(n.right, t.key)
            return n
        self.root = _delete(self.root, key)

class AVLTree(BinarySearchTree):
    def get_h(self, n): return n.height if n else 0
    def get_b(self, n): return self.get_h(n.left) - self.get_h(n.right)

    def rotate_left(self, x):
        y, x.right, y.left = x.right, x.right.left, x
        x.height, y.height = 1 + max(self.get_h(x.left), self.get_h(x.right)), 1 + max(self.get_h(y.left), self.get_h(y.right))
        return y

    def rotate_right(self, y):
        x, y.left, x.right = y.left, y.left.right, y
        y.height, x.height = 1 + max(self.get_h(y.left), self.get_h(y.right)), 1 + max(self.get_h(x.left), self.get_h(x.right))
        return x

    def insert_node(self, key):
        def _insert(n, k):
            if not n: return Node(k)
            if k < n.key: n.left = _insert(n.left, k)
            elif k > n.key: n.right = _insert(n.right, k)
            else: return n
            n.height = 1 + max(self.get_h(n.left), self.get_h(n.right))
            b = self.get_b(n)
            if b > 1: return self.rotate_right(n) if k < n.left.key else self.rotate_right(self._left(n))
            if b < -1: return self.rotate_left(n) if k > n.right.key else self.rotate_left(self._right(n))
            return n
        self.root = _insert(self.root, key)

    def delete_node(self, key):
        def _min(n):
            while n.left: n = n.left
            return n
        def _delete(n, k):
            if not n: return n
            if k < n.key: n.left = _delete(n.left, k)
            elif k > n.key: n.right = _delete(n.right, k)
            else:
                if not n.left: return n.right
                if not n.right: return n.left
                t = _min(n.right)
                n.key = t.key
                n.right = _delete(n.right, t.key)
            n.height = 1 + max(self.get_h(n.left), self.get_h(n.right))
            b = self.get_b(n)
            if b > 1: return self.rotate_right(n) if self.get_b(n.left) >= 0 else self.rotate_right(self._left(n))
            if b < -1: return self.rotate_left(n) if self.get_b(n.right) <= 0 else self.rotate_left(self._right(n))
            return n
        self.root = _delete(self.root, key)

    def _left(self, n): n.left = self.rotate_left(n.left); return n
    def _right(self, n): n.right = self.rotate_right(n.right); return n

RED, BLACK = True, False

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, BLACK)
        self.root = self.NIL

    def insert_node(self, key):
        n = Node(key, RED); n.left = n.right = self.NIL
        y, x = None, self.root
        while x != self.NIL:
            y, x = x, x.left if n.key < x.key else x.right
        n.parent = y
        if not y: self.root = n
        elif n.key < y.key: y.left = n
        else: y.right = n
        self._fix_insert(n)

    def delete_node(self, key):
        def _min(n):
            while n.left != self.NIL: n = n.left
            return n
        def _transplant(u, v):
            if not u.parent: self.root = v
            elif u == u.parent.left: u.parent.left = v
            else: u.parent.right = v
            v.parent = u.parent
        z = self.root
        while z != self.NIL and z.key != key:
            z = z.left if key < z.key else z.right
        if z == self.NIL: return
        y, y_color, x = z, z.color, None
        if z.left == self.NIL:
            x = z.right
            _transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            _transplant(z, z.left)
        else:
            y = _min(z.right)
            y_color = y.color
            x = y.right
            if y.parent == z: x.parent = y
            else:
                _transplant(y, y.right)
                y.right, y.right.parent = z.right, y
            _transplant(z, y)
            y.left, y.left.parent, y.color = z.left, y, z.color
        if y_color == BLACK: self._fix_delete(x)

    def _fix_insert(self, z):
        while z != self.root and z.parent.color == RED:
            p, g = z.parent, z.parent.parent
            u = g.right if p == g.left else g.left
            if u.color == RED:
                p.color = u.color = BLACK; g.color = RED; z = g
            else:
                if (p == g.left and z == p.right): z = p; self._rotate_left(z)
                elif (p == g.right and z == p.left): z = p; self._rotate_right(z)
                p.color, g.color = BLACK, RED
                if p == g.left: self._rotate_right(g)
                else: self._rotate_left(g)
        self.root.color = BLACK

    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == RED:
                    s.color, x.parent.color = BLACK, RED
                    self._rotate_left(x.parent)
                    s = x.parent.right
                if s.left.color == BLACK and s.right.color == BLACK:
                    s.color = RED; x = x.parent
                else:
                    if s.right.color == BLACK:
                        s.left.color, s.color = BLACK, RED
                        self._rotate_right(s)
                        s = x.parent.right
                    s.color, x.parent.color, s.right.color = x.parent.color, BLACK, BLACK
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == RED:
                    s.color, x.parent.color = BLACK, RED
                    self._rotate_right(x.parent)
                    s = x.parent.left
                if s.left.color == BLACK and s.right.color == BLACK:
                    s.color = RED; x = x.parent
                else:
                    if s.left.color == BLACK:
                        s.right.color, s.color = BLACK, RED
                        self._rotate_left(s)
                        s = x.parent.left
                    s.color, x.parent.color, s.left.color = x.parent.color, BLACK, BLACK
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = BLACK

    def _rotate_left(self, x):
        y = x.right; x.right = y.left
        if y.left != self.NIL: y.left.parent = x
        y.parent = x.parent
        if not x.parent: self.root = y
        elif x == x.parent.left: x.parent.left = y
        else: x.parent.right = y
        y.left, x.parent = x, y

    def _rotate_right(self, y):
        x = y.left; y.left = x.right
        if x.right != self.NIL: x.right.parent = y
        x.parent = y.parent
        if not y.parent: self.root = x
        elif y == y.parent.right: y.parent.right = x
        else: y.parent.left = x
        x.right, y.parent = y, x

if __name__ == "__main__":
    bst = BinarySearchTree()
    for k in [20, 10, 30, 5, 15]: bst.insert_node(k)
    assert bst.search_node(10) and not bst.search_node(99)
    bst.delete_node(10); assert not bst.search_node(10)

    avl = AVLTree()
    for k in [10, 20, 30, 40, 50, 25]: avl.insert_node(k)
    assert avl.root.key == 30
    avl.delete_node(40); assert not avl.search_node(40)

    rbt = RedBlackTree()
    for k in [20, 15, 25, 10, 5]: rbt.insert_node(k)
    assert rbt.root.key == 20 and rbt.root.color == BLACK
    rbt.delete_node(15)

    print("Test cases were executed sucessfully")
