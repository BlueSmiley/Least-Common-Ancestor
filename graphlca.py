
class LCAGraph(object):
    """
    Create graphs with which the lowest common ancestor of nodes can be found

    Offers functionality to add nodes and edges between nodes to an instance
    of the class which represents a directed acyclic graph.
    Allows keys of any type for nodes as long as __eq__ and __hash__ is 
    implemented and the key is not None.
    Graph represented by a binary tree where each node can only have 
    a maximum of two child nodes.
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
        """Returns if a key is a viable key for a node in the graph"""
        return key != None
    
    def existing_node(self,key):
        """Returns whether a node exists in the graph or not"""
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

        if self.existing_node(src_node):
            if dest_node in self.edges(src_node):
                return False
            if (self.existing_node(dest_node) and 
                self.descendant(dest_node,src_node)):
                    return False
            if not self.existing_node(dest_node):
                self.add_node(dest_node)
            self.graph[src_node].append(dest_node)
            return True
        else:
            return False
    
    def descendant(self,src_node,dest_node):
        """Finds if a node is a descendant of another node in a graph
        
        Searches through graph to see if a target node is either the child of a 
        chosen node or the child of a node that is itself a child of the chosen
        node.

        Args:
            src_node: The chosen node from which the search begins
            dest_node: The target node being checked if is a descendant of the
                src_node
        
        Returns:
            A boolean representing whether the target node is a descendant of
            the chosen node or not.
        """
        if src_node == dest_node:
            return True
        for child in self.edges(src_node):
            if self.descendant(child,dest_node):
                return True
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

        # Method to remove duplicate elements from list
        # Requires elements implement __hash__() and __eq__() correctly
        # Which is required by a dictionary anyway to store the nodes
        # So no extra constraints introduced by operation
        # A set has no duplicate elements so converting to set removes dupes
        # Then conversion back into list so we can expicitly treat it as list
        nodelist = list(set(nodelist))
        # Minor performance optimisation
        if(len(nodelist)==0):
            return None
        result = self.lca(root,nodelist,[],0,(-1,None),(-1,None))
        lcatuple = result[1]
        if lcatuple[1] != None:
            return lcatuple[1]
        return None

    # Performs euler tour of graph and finds common ancestors as it continues
    # Picks the ancestor with greatest depth as it goes along
    # Therefore final common ancestor is the least common ancestor
    def lca(self,current,nodelist,matchedlist,depth,foundlowest,currentlowest):
        """Recursive function to find lowest common ancestor
        
        Recursive function to find lowest common ancestor of target nodes 
        called initially by Lowest_common_ancestor with default values. 
        Computes only a single lowest common ancestor of the graph.

        Args:
            current: Current node on which the function is being called.
            nodelist: List of target nodes.
            matchedlist: List of target nodes found so far during search.
                Used internally for recognizing euler tours that match nodes.
                Cleared after all nodes in nodelist matched
            depth: Number of hops/edges from the root node for the current
                node
            foundlowest: Tuple that contains the node and the depth of the 
                node that is the lowest common ancestor with greatest depth
                found so far.
            currentlowest: Tuple that contains the node and the depth of the
                node that is the node, with the lowest depth found in current
                euler tour starting from the first matched node.
         
        Returns:
            A tuple of (matchedlist,foundlowest and currentlowest), where 
            foundlowest and currentlowest are themselves tuples of the format 
            described above.
        """
        if current in nodelist and current not in matchedlist:
            matchedlist.append(current)
            # if first match then lowest depth = current node
            if len(matchedlist) == 1:
                currentlowest = (depth,current)
        # If all matched and we find lca with greater depth then replace
        # Clear matchedlist to show euler tour between target nodes complete
        if len(matchedlist) == len(nodelist):
            if currentlowest[0] > foundlowest[0]:
                foundlowest = currentlowest 
            matchedlist = []
        # Continue dfs/euler tour of entire tree
        for child in self.edges(current):
            # replace matchedlist,foundlowest and currentlowest with result
            # of euler tour of child nodes
            matchedlist,foundlowest,currentlowest = self.lca(child,nodelist,
                matchedlist,depth+1,foundlowest,currentlowest)
            # Repeat almost same procedure used at start 
            if current in nodelist and current not in matchedlist:
                matchedlist.append(current)
                if len(matchedlist) == 1:
                    currentlowest = (depth,current)
            # If still in matching phase and recursed to node with less depth,
            # then lca always node with lowest level that is found during euler 
            # tour between target nodes
            if len(matchedlist) > 0 and depth < currentlowest[0]:
                currentlowest = (depth,current)
            # Never going to recurse to a target branch to match last node
        
        return matchedlist,foundlowest,currentlowest
        

        

