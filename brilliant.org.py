# Vir: https://brilliant.org/wiki/scapegoat-tree/

import math
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class Scapegoat:
    def __init__(self):
        self.root = None
        self.size = 0
        self.maxSize = 0

    def insert(self, key):
        node = Node(key)
        #Base Case - Nothing in the tree
        if self.root == None:
            self.root = node
            return
        #Search to find the node's correct place
        currentNode = self.root
        while currentNode != None:
            potentialParent = currentNode
            if node.key < currentNode.key:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right
        #Assign parents and siblings to the new node
        node.parent = potentialParent
        if node.key < node.parent.key:
            node.parent.left = node
        else:
            node.parent.right = node
        node.left = None
        node.right = None
        self.size += 1
        scapegoat = self.findScapegoat(node)
        if scapegoat == None:
            return
        tmp = self.rebalance(scapegoat)

        #Assign the correct pointers to and from scapegoat
        scapegoat.left = tmp.left
        scapegoat.right = tmp.right
        scapegoat.key = tmp.key
        scapegoat.left.parent = scapegoat
        scapegoat.right.parent = scapegoat

    def findScapegoat(self, node):
        if node == self.root:
            return None
        while self.isBalancedAtNode(node) == True:
            if node == self.root:
                return None
            node = node.parent
        return node

    def isBalancedAtNode(self, node):
        if abs(self.sizeOfSubtree(node.left) - self.sizeOfSubtree(node.right)) <= 1:
            return True
        return False

    def sizeOfSubtree(self, node):
        if node == None:
            return 0
        return 1 + self.sizeOfSubtree(node.left) + self.sizeOfSubtree(node.right)

    def rebalance(self, root):
        def flatten(node, nodes):
            if node == None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)

        def buildTreeFromSortedList(nodes, start, end):
            if start > end:
                return None
            mid = int(math.ceil(start + (end - start) / 2.0))
            node = Node(nodes[mid].key)
            node.left = buildTreeFromSortedList(nodes, start, mid-1)
            node.right = buildTreeFromSortedList(nodes, mid+1, end)
            return node

        nodes = []
        flatten(root, nodes)
        return buildTreeFromSortedList(nodes, 0, len(nodes)-1)

    def delete(self, key):
        pass