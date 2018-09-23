class LCAGraph:
    #Constructor
    def __init__(self):
        self.graph = {}

    def add_node(self,key):
        if key in self.graph:
            return False
        else:
            self.graph[key] = []    #empty list for orphaned nodes
            return True

    def add_edge(self,src_node,dest_node):
        if src_node not in self.graph:
            self.add_node(src_node)
        if dest_node not in self.graph[src_node]:
            self.graph[src_node].append(dest_node)
            return True
        else:
            return False
    
    def lowest_common_ancestor(self,root,node1,node2):
        nodelist = []
        node = self.lca(root,node1,node2,nodelist)
        if(sorted(nodelist) == sorted([node1,node2])):
            return node
        return None

    #credit to https://dxmahata.gitbooks.io/leetcode-python-solutions/lowest_common_ancestor_in_a_binary_tree.html for solution
    def lca(self,root,node1,node2,nodelist):
        #recurse when reach null node
        if root == None:
            return None
        #for end comparison to see if all nodes are in same component
        if root == node1 or root == node2:
            nodelist.append(root)
        #recursive search through tree
        left = self.lca(self.graph[root][0],node1,node2,nodelist)
        right = self.lca(self.graph[root][1],node1,node2,nodelist)

        #if a node found on both sides then replace lca with this node
        if(left != None and right != None):
            return root
        #if root == node then return root
        elif root == node1 or root == node2:
            return root
        #else return whichever side has the node or if neither then return None
        elif left != None:
            return left
        else:
            return right
        

