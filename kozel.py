from IPython.display import display
import math

class Node:
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None

class GresniKozel:
    def __init__(self,alfa=0.7): 
        self.root = None
        self.maxSize = 0
        self.alfa = alfa

        self.nodeCount = 0 # te dve sta za deletion
        self.maxNodeCount = 0

        self.pregloboko = False # uporabimo pri insertu ce gremo pregloboko
        self.insert_otrok_size = 0 # pri insertu da ugotovimo velikost otrok

    def find(self,val): # isto kot pr bstju
        cur = self.root
        while cur != None and cur.val != val:
            if val > cur.val: cur = cur.right
            else: cur = cur.left 
        return cur.val if cur != None else cur 
    
    def insert(self, val):
        if self.root == None: 
            self.root = Node(val)
            self.nodeCount=1
            self.maxNodeCount=1
            return 
        self.pregloboko = False
        self.insert_otrok_size = 0
        (gresni_kozel,stars) = self._insert_return_kozel(self.root,val,1,None)
        if gresni_kozel == None: return
        nov_kozel = self._uravnovesi(gresni_kozel)
        # povezemo to poddrevo na original
        if stars is None: # mal nadlezno ker mormo vedt tut starsa ampak pac tko je
            self.root = nov_kozel
        elif stars.left == gresni_kozel:
            stars.left = nov_kozel
        else: stars.right = nov_kozel

    def remove(self, val):
        self.root, removed = self._remove(self.root, val)

        if removed:
            self.nodeCount -= 1

            # trigger rebuild condition
            if self.nodeCount <= self.maxNodeCount // 2:
                self.root = self._uravnovesi(self.root)
                self.maxNodeCount = self.nodeCount

    def _insert_return_kozel(self,node, val, depth, parent):
        if val == node.val: return (None,None)
        kozel = (None,None)
        if val > node.val: 
            if node.right == None:
                node.right = Node(val)
                self.nodeCount+=1
                self.maxNodeCount = max(self.maxNodeCount,self.nodeCount)
                self.pregloboko = depth+1 > math.floor(math.log(self.nodeCount,1/self.alfa)) # pogoj na max globini
            else: kozel = self._insert_return_kozel(node.right,val,depth+1,node)
        elif val < node.val:
            if node.left == None:
                node.left = Node(val)
                self.nodeCount+=1
                self.maxNodeCount = max(self.maxNodeCount,self.nodeCount)
                self.pregloboko = depth+1 > math.floor(math.log(self.nodeCount,1/self.alfa)) # pogoj na max globini
            else: kozel = self._insert_return_kozel(node.left,val,depth+1,node)

        if self.pregloboko == False: return (None,None)
        if kozel != (None,None): return kozel
        # na tej tocki smo ze insertal in nazaj gor iscemo kozla
        # trenutna noda je kozel ce vsaj en izmed otrok ne izpolnjuje
        # pogoja |O| <= alfa*|S|
        # vemo ze velikost enega otroka, moramo samo se ugotoviti velikost drugega
        levi = 0
        desni = 0
        if val > node.val: 
            desni = self.insert_otrok_size
            levi = self._get_subtree_size(node.left)
        else: 
            desni = self._get_subtree_size(node.right)
            levi = self.insert_otrok_size
        node_size = levi+desni+1
        self.insert_otrok_size = node_size # for posteriority

        # pogoj za uravnotezenost 
        uravnotezen = True
        uravnotezen &= levi <= self.alfa * node_size
        uravnotezen &= desni <= self.alfa * node_size

        return (None,None) if uravnotezen else (node,parent) # ce smo nasli kozla ga passamo nazaj

    def _get_subtree_size(self,node):
        if node == None: return 0
        return self._get_subtree_size(node.left) + self._get_subtree_size(node.right) + 1

    def _min(self, node):
        while node.left:
            node = node.left
        return node

    def _remove(self, node, val):
        if node is None:
            return None, False

        removed = False

        if val < node.val:
            node.left, removed = self._remove(node.left, val)
        elif val > node.val:
            node.right, removed = self._remove(node.right, val)
        else:
            removed = True

            # 0 or 1 child
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True

            # 2 children → replace with inorder successor
            succ = self._min(node.right)
            node.val = succ.val
            node.right, _ = self._remove(node.right, succ.val)

        return node, removed

    def _uravnovesi(self,node):
        # torej to poddrevo flattenamo v array
        # in ga rekonstruiramo
        def flatten(node, nodes):
            if node == None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)
        
        def drevo_from_sorted_list(nodes, start, end):
            if start > end:
                return None
            mid = (start + end) // 2
            noda = nodes[mid]
            noda.left = drevo_from_sorted_list(nodes, start, mid-1)
            noda.right = drevo_from_sorted_list(nodes, mid+1, end)
            return noda

        nodes = []
        flatten(node, nodes)
        for u in nodes:
            u.left = None
            u.right = None
        return drevo_from_sorted_list(nodes, 0, len(nodes)-1)

    def draw(self):
        def _display(node):
            if node is None:
                return [" "], 1, 1, 0  # lines, width, height, middle

            line = str(node.val)
            line_len = len(line)

            # Leaf
            if node.left is None and node.right is None:
                return [line], line_len, 1, line_len // 2

            # Left subtree
            left, n, p, x = _display(node.left)
            # Right subtree
            right, m, q, y = _display(node.right)

            # Build connections
            first_line = (x + 1) * " " + (n - x - 1) * "_" + line + y * "_" + (m - y) * " "
            second_line = x * " " + "/" + (n - x - 1 + line_len + y) * " " + "\\" + (m - y - 1) * " "

            # Merge lines
            if p < q:
                left += [" " * n] * (q - p)
            elif q < p:
                right += [" " * m] * (p - q)

            zipped = zip(left, right)
            lines = [first_line, second_line] + [a + line_len * " " + b for a, b in zipped]

            return lines, n + m + line_len, max(p, q) + 2, n + line_len // 2

        lines, *_ = _display(self.root)
        display("\n".join(lines))


def main():
    drevo = GresniKozel()
    for i in range(0, 100, 10):
        drevo.insert(i)
        drevo.draw()
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


    drevo.insert(42)
    drevo.draw()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    drevo.remove(42)
    drevo.draw()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    drevo.remove(20)
    drevo.draw()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    drevo.remove(10)
    drevo.draw()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    drevo.remove(0)
    drevo.draw()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    drevo.remove(50)
    drevo.draw()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    drevo.remove(30)
    drevo.draw()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


main()