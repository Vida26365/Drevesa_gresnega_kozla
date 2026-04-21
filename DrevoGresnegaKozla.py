import html as _html
from IPython.display import HTML, display
import math


class Noda:
    def __init__(self, key): #To je vse kar potrebujemo za nodo
        self.key = key
        self.left = None
        self.right = None
        
        
    def _html_node_row_(self):
        return f"<hd>{self.key}</hd><td>{self.left}</td><td>{self.right}</td>"
    
    def povezi(self, stars):
        if self.key < stars.key:
            stars.left = self
        else:
            stars.right = self

   
class GresniKozel:
    def __init__(self): # To je vse kar potrebujemo za drevo
        self.root = None
        self.size = 0
        self.maxSize = 0
        
        self.stack = []
        
    def najdi(self, key, prikazi):
        def _pom(root):
            if root == None:
                return False
            self.stack.append(root)
            if prikazi: self.prikazi(root)
            if key == root.key:
                if prikazi: self.prikazi(root, False)
                return root
            if key < root.key:
                return _pom(root.left)
            else:
                return _pom(root.right)
        return _pom(self.root)
        
    def vrini(self, key, prikazi=False):
        
        noda = Noda(key)
        # noda.left = None
        # noda.right = None
        
        if prikazi: self.naslov("Iskanje starša", 2)
        
        # Rekurzivno iskanje
        def _najdi_mesto_node_za_vstavit(root, noda, prikazi = False):
            if prikazi == True:
                self.prikazi(root)
            if root == None:
                return 
            self.stack.append(root)
            if noda.key < root.key:
                if root.left == None:
                    return root
                return _najdi_mesto_node_za_vstavit(root.left, noda, prikazi)
            else:
                if root.right == None:
                    return root
                return _najdi_mesto_node_za_vstavit(root.right, noda, prikazi)
            
            
        stars = _najdi_mesto_node_za_vstavit(self.root, noda, prikazi)
        
        if stars == None:
            self.root = noda
        else:
            noda.povezi(stars)
        
        self.size += 1
        self.maxSize = max(self.maxSize, self.size)
        
        if prikazi: self.prikazi()
    
    
    def velikost_poddrevesa(self, node):
        if node == None:
            return 0
        return 1 + self.velikost_poddrevesa(node.left) + self.velikost_poddrevesa(node.right)


    def je_uravnovesena_noda(self, noda, prikazi = False):
        if abs(self.velikost_poddrevesa(noda.left) - self.velikost_poddrevesa(noda.right)) <= 1:
            if prikazi: self.prikazi(noda, False)
            return True
        if prikazi: self.prikazi(noda, True)
        return False
    
            
    
    def gresni_kozel(self,  prikazi=False):
        if prikazi: self.naslov("Najdi grešnega kozla", 2)
        if self.stack == []:
            return None
        noda = self.stack.pop()
        while self.je_uravnovesena_noda(noda, prikazi) == True and self.stack != []:
            if noda == self.root:
                return None
            noda = self.stack.pop() # Gre do starša
        return noda

    
    def uravnovesi(self, root):
        def flatten(node, nodes):
            if node == None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)

        def drevo_from_sorted_list(nodes, start, end):
            if start > end:
                return None
            mid = int(math.ceil(start + (end - start) / 2.0))
            # node = Node(nodes[mid].key)
            noda = nodes[mid]
            noda.left = drevo_from_sorted_list(nodes, start, mid-1)
            noda.right = drevo_from_sorted_list(nodes, mid+1, end)
            return noda

        nodes = []
        flatten(root, nodes)
        return drevo_from_sorted_list(nodes, 0, len(nodes)-1)



    
    def vstavi(self, key, prikaz =  False):
        self.vrini(key, prikaz)
        koza = self.gresni_kozel(prikaz)
        koza = self.uravnovesi(koza)
        if koza != None:
            if self.stack != []:
                stars = self.stack.pop()
                koza.povezi(stars)
            else:
                self.root = koza
        self.stack = []
        if prikaz:
            self.prikazi()
            
    def odstrani(self, key, prikazi):
        self.stack = []
        noda = self.najdi(key, prikazi)
        if noda == False:
            return False
        
        stars = None
        if self.stack != []:
            stars = self.stack.pop()
        
        def _ekstrem_od(noda, desnanje):
                if desnanje: stranski_otrok = noda.left
                else: stranski_otrok = noda.right
            
                if stranski_otrok == None:
                    if prikazi: self.prikazi(noda, False)
                    return noda
                self.stack.append(noda)
                if prikazi: self.prikazi(noda)
                return _ekstrem_od(stranski_otrok, desnanje)
            

        def _odstranjevanje(noda, stars):
            if noda == None:
                return
            
            if noda.left == None and noda.right == None:
                if stars == None:
                    self.root = noda
                if noda.key < stars.key: stars.left = None
                else: stars.right = None
            
            self.stack = []
            if noda.right != None:
                ekstrem = _ekstrem_od(noda.right, True)
            elif noda.left != None:
                ekstrem =_ekstrem_od(noda.left, False)
            else:
                noda = None
                return
                
            noda.key = ekstrem.key
            if self.stack == []:
                stars_ekstrema = None
            else:
                stars_ekstrema =self.stack.pop()
            _odstranjevanje(ekstrem, stars_ekstrema)
        
         
        _odstranjevanje(noda, stars)
        
            
               
        
        # stars = None
        # if self.stack != []:
        #     stars = self.stack.pop()
        # def _zamakni(stars, nov_otrok):
                
        #     if nov_otrok.left == None:
        #         zamenjava = noda.right
        #     else:
        #         zamenjava = noda.left
            
        #     if stars == None:
        #         self.root == zamenjava
        
        
        # def _odstrani_bst(node, key):
        #     if node is None:
        #         return None, False

        #     if key < node.key:
        #         node.left, removed = _odstrani_bst(node.left, key)
        #         return node, removed

        #     if key > node.key:
        #         node.right, removed = _odstrani_bst(node.right, key)
        #         return node, removed

        #     # Noda z enim otrokom ali brez otrok.
        #     if node.left is None:
        #         return node.right, True
        #     if node.right is None:
        #         return node.left, True

        #     # Noda z dvema otrokoma: nadomesti jo naslednik (min v desnem poddrevesu).
        #     naslednik_stars = node
        #     naslednik = node.right
        #     while naslednik.left is not None:
        #         naslednik_stars = naslednik
        #         naslednik = naslednik.left

        #     node.key = naslednik.key
        #     if naslednik_stars == node:
        #         naslednik_stars.right = naslednik.right
        #     else:
        #         naslednik_stars.left = naslednik.right
        #     return node, True

        # self.root, removed = _odstrani_bst(self.root, key)
        # if not removed:
        #     return False

        # self.size -= 1
        # if self.size == 0:
        #     self.root = None
        #     self.maxSize = 0
        #     return True

        # # Scapegoat pravilo po brisanju: če je drevo preveč skrčeno glede na maxSize,
        # # uravnovesi celotno drevo in posodobi maxSize.
        # if self.size < self.maxSize / 2:
        #     self.root = self.uravnovesi(self.root)
        #     self.maxSize = self.size

        # return True
    
    
    
    

    def prikazi(self, node=None, scape=None):
        def prikazi_stack():
            css = """
            <style>
            table, th, td {
                border: 1px solid white;
            }
            </style>
            """
            html = ""
            for noda in self.stack:
                html += f"<td>{noda.key}</td>"
            htmlk = f"Kopica: {css}<table><tr>{html}</tr></table>"
            return htmlk
            # display(HTML(htmlk))

        if self.root is None:
            display(HTML("<p>Tree is empty.</p>"))
            return

        coords = {}
        order = [0]
        max_depth = [0]

        def assign_positions(node, depth=0):
            if node is None:
                return
            assign_positions(node.left, depth + 1)
            coords[node] = (order[0], depth)
            order[0] += 1
            max_depth[0] = max(max_depth[0], depth)
            assign_positions(node.right, depth + 1)

        assign_positions(self.root)

        x_step = 80
        y_step = 90
        margin = 40
        radius = 18

        width = margin * 2 + max(1, order[0] - 1) * x_step + 2 * radius
        height = margin * 2 + max_depth[0] * y_step + 2 * radius

        def node_pixel(node):
            x_idx, depth = coords[node]
            x = margin + x_idx * x_step + radius
            y = margin + depth * y_step + radius
            return x, y

        parts = []

        def draw_edges(node):
            if node is None:
                return
            x1, y1 = node_pixel(node)
            if node.left is not None:
                x2, y2 = node_pixel(node.left)
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#444" stroke-width="2"/>')
                draw_edges(node.left)
            if node.right is not None:
                x2, y2 = node_pixel(node.right)
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#444" stroke-width="2"/>')
                draw_edges(node.right)

        def draw_nodes(current_node):
            if current_node is None:
                return
            x, y = node_pixel(current_node)
            label = _html.escape(str(current_node.key))
            fill_color = '#e6f2ff'
            stroke_color = '#2b6cb0'
            if node is not None and current_node is node:
                if scape == None:
                    fill_color = "#ffb3fe"
                    stroke_color = "#ce28b3"
                else:
                    fill_color = '#ffd6d6' if scape else '#d9f7d9'
                    stroke_color = '#c53030' if scape else '#2f855a'
            parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="2"/>')
            parts.append(f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#1a202c">{label}</text>')
            draw_nodes(current_node.left)
            draw_nodes(current_node.right)

        draw_edges(self.root)
        draw_nodes(self.root)

        svg = f"""
        <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="{width}" height="{height}" fill="white"/>
            {''.join(parts)}
        </svg>
        """
        
        display(HTML(prikazi_stack()))
        display(HTML(svg))
            

    def naslov(self, niz, i=1):
        html = f"<h{i}>{niz}<h{i}>"
        display(HTML(html))