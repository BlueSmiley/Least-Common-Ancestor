from collections import Counter

class LCAGraph(object):
    """
    Create graphs with which the lowest common ancestor of nodes can be found

    Offers functionality to add nodes and edges between nodes to an instance
    of the class which represents a directed acyclic graph. Allows keys of any
    type for nodes as long as __eq__ is implemented and the key is not None.
    Graph represented by a binary tree where each node can only have a maximum
    of two child nodes.

    Edges to non-existent nodes instantiates the node as a new node
    """

    def __init__(self):
        """Initialises data structure to hold graph nodes and edges"""
        self.graph = {}

    # Initialise an empty list on creation representing the adjacency list of
    # a vertex. Each external vertex added to this list represents a directed 
    # edge from this vertex to that external vertex. 
    def add_node(self,key):
        """Adds a new node to the graph given a key 
        
        Adds a node using the given key if the key is viable and no node
        already exits with the given key

        Args:
            key: A unique value to identify the new node in the graph.

        Returns:
            A boolean representing whether a new node was sucessfully added
            or failed.
        """

        if not self.viable_key(key) or self.existing_node(key):
            return False
        else:
            self.graph[key] = []    
            return True

    def viable_key(self,key):
        return key != None
    
    def existing_node(self,key):
        return  self.viable_key(key) and key in self.graph

    # Append destination vertex to adjacency list of source vertex
    # to represent a directed edge from source to destination vertex
    def add_edge(self,src_node,dest_node):
        """Adds an edge between two nodes

        Adds a directed edge between the source node and destination node.
        Creates a new node if the destination node doesn't already exist.
        Operation fails if the source node already has two links, 
        destination node key is invalid or if the source node doesn't exist.

        Args:
            src_node: A key which identifies the source node from which the
                edge begins.
            dest_node: A key which identifies the destination node of the edge.
        
        Returns:
            A boolean representing whether the operation to add the edge 
            succeeded or failed.
        """

        if( self.existing_node(src_node) and len(self.graph[src_node]) < 2):
            for node in self.graph:
                if dest_node in self.edges(node):
                    return False
            if not self.existing_node(dest_node):
                self.add_node(dest_node)
            self.graph[src_node].append(dest_node)
            return True
        else:
            return False
    
    def edges(self,node):
        """Returns all directed edges from the corresponding node"""
        return self.graph[node]

    def lowest_common_ancestor(self,root,nodelist):
        """Finds the lowest common ancestor of set of nodes from a root node

        Finds the lowest common ancestor of a set of nodes from a root node if
        it exists. Searches the subgraph consisting of the children of the node 
        passed as root for the presence of the entire set of nodes to match. 
        Returns the lowest common ancestor of those nodes if entire set can be 
        found in the subgraph.

        Args:
            root: The node which is treated as the root of the subgraph/tree
            nodelist: A list which contains all target nodes of which the 
                lowest common ancestor should be found of.
        
        Returns:
            Either the key of the node which is the lowest common ancestor
            of the target nodes or None to represent failure to find the
            lowest common ancestor.
        """

        nodelist = list(set(nodelist))
        matchedlist = []
        node = self.lca(root,nodelist,matchedlist)
        if(Counter(set(nodelist)) == Counter(set(matchedlist))):
            return node
        return None

    #credit to https://dxmahata.gitbooks.io/leetcode-python-solutions/lowest_common_ancestor_in_a_binary_tree.html for solution
    def lca(self,root,nodelist,matchedlist):
        """Recursive function to find lowest common ancestor
        
        Recursive function to find lowest common ancestor of target nodes 
        called initially by Lowest_common_ancestor with default values. 

        Args:
            root: Current node on which the function is being called.
            nodelist: List of target nodes.
            matchedlist: List of target nodes found so far during search
        
        Returns:
            Modifies the matchedlist whenever a target node is found. Returns 
            None if no target node found in the current node or children of the 
            current node. Returns the current node itself if a child found in 
            both left and right subtrees or if the current node itself is a 
            target node. Else if the return value of the function call on the 
            left subtrees is not None it returns the return value. Else it 
            returns the return value of the function call on the right subtree.

        """

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

        #if root == node then return root
        #also add node to list of found nodes to check at end if all found
        for node in nodelist:
            if root == node:
                matchedlist.append(root)
                return root

        #if a node found on both sides then replace lca with this node
        if(left != None and right != None):
            return root

        #else return whichever side has the node or if neither then return None
        if left != None:
            return left
        else:
            return right
        

