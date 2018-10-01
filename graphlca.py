class LCAGraph(object):
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
        self.add_node(src_node)
        self.add_node(dest_node)
        if( len(self.graph[src_node]) < 2 and 
                dest_node not in self.graph[src_node]):
            self.graph[src_node].append(dest_node)
            return True
        else:
            return False
    
    def edges(self,node):
        return self.graph[node]

    def lowest_common_ancestor(self,root,nodelist):
        nodelist = list(set(nodelist))
        matchedlist = []
        node = self.lca(root,nodelist,matchedlist)
        if(set(nodelist) == set(matchedlist)):
            return node
        return None

    #credit to https://dxmahata.gitbooks.io/leetcode-python-solutions/lowest_common_ancestor_in_a_binary_tree.html for solution
    def lca(self,root,nodelist,matchedlist):
        #recurse when reach null node
        if root == None:
            return None
        #recursive search through tree
        if len(self.graph[root]) > 0:
            left = self.lca(self.graph[root][0],nodelist,matchedlist)
        else:
            left = None
        if len(self.graph[root]) > 1:
            right = self.lca(self.graph[root][1],nodelist,matchedlist)
        else:
            right = None

        #if a node found on both sides then replace lca with this node
        if(left != None and right != None):
            return root
        #if root == node then return root
        #also add node to list of found nodes to check at end if all found
        for node in nodelist:
            if root == node:
                matchedlist.append(root)
                return root
        #else return whichever side has the node or if neither then return None
        if left != None:
            return left
        else:
            return right
        

