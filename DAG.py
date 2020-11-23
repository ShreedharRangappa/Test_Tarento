

class CreateGraph():
    ''' ASSUMPTION: The direction of link between vertices are always downwards'''
    def __init__(self):
        self.graph_dict = dict()


    def get_vertices(self):
        return self.graph_dict.keys()

    # Is a vertices is linked with any other
    def isdependent(self, vert):
        nodes=self.graph_dict[vert]
        if len(nodes)==0:
            return False
        else:
            return True


    def add_vertices(self,start,end, status_update=False):
        start,end=map(str,(start,end))
        if start not in self.get_vertices():
            self.graph_dict[start]=[]
        if end not in self.get_vertices():
            self.graph_dict[end]=[]
        self.graph_dict[start].append(end)
        if status_update:
            print(f'Done: {start}--> {end}')

    def find_index(self,key,paths):
        idxs=[]
        for ith, val in enumerate(paths):
            if key in paths[ith]:
                idxs.append(ith)

        return idxs

    def remove_vert_dict(self, vert):
        # Remove the key pair
        self.graph_dict.pop(vert)
        # Remove the link
        for dk in self.graph_dict.keys():
            if  vert in self.graph_dict[dk]:
                temp=self.graph_dict[dk]
                temp.remove(vert)
                self.graph_dict[dk]=temp

    def merge_vert_dict(self, r_vert, j_vert):
        # Dict key to be removed
        r_links=self.graph_dict[r_vert]

        # Joining Dict
        j_links=self.graph_dict[j_vert]

        # Merge multiple entries
        for j_l in j_links:
            if j_l in r_links:
                r_links.pop(j_l)

        for r_l in r_links:
            self.graph_dict[j_vert].append(r_l)


        # Remove the verticies
        self.remove_vert_dict(r_vert)



    def remove_verticies(self, verticies, join_to=None, remove_with_links=False):
        '''
        :param verticies: location, which needs to be removed from the graph
        :param join_to: location, after removing verticies dependent links to be joined to
        :return: Updated graph
        '''
        if join_to:
            verticies,join_to=map(str,(verticies,join_to))
        else:
            verticies=str(verticies)

        # Is verticies available
        if verticies not in self.get_vertices():
            print(f'"{verticies}" to be removed is not available')
            return
        if join_to:
            if join_to not in self.get_vertices():
                print(f'"{verticies}" is not available for updating')
                return

        status = self.isdependent(verticies)
        if not status:
            # Just remove the verticies
            self.remove_vert_dict(verticies)
        elif status and remove_with_links:
            # Remove the verticies and single dependencies
            self.remove_vert_dict(verticies)
        else:
            # Remove verticies and join the dependent links
            self.merge_vert_dict(verticies, join_to)


    def get_graph(self):
        return self.graph_dict



class DecodeGraph(CreateGraph):
    def __init__(self,graph):
        super().__init__()
        status=self.validate_graph(graph)
        if status:
            if len(graph)==0:
                print('Graph is empty')
            self.graph_dict=graph
        else:
            print('Graph format/content is not accepted')


    def validate_graph(self,graph):
        if type(graph) is dict:
            return True
        else:
            return False


    def print_paths(self):
        '''order of key pairs represent the graph structure'''
        paths=[]
        for i,dk in enumerate(self.get_vertices()):

            if i ==0:
                for neighbour in self.graph_dict[dk]:
                    paths.append(dk+neighbour)
            else:
                idxs = self.find_index(dk,paths)
                temp = paths[idxs[0]]
                if len(self.graph_dict[dk])>1:
                    for j in range(len(self.graph_dict[dk])-1):
                        paths.append(temp)
                        idxs.append(len(paths)-1)

                for idx,neighbour in zip(idxs,self.graph_dict[dk]) :
                    paths[idx]+=neighbour


        for path in paths:
            p_len=len(path)
            temp=''
            for pi,pat in enumerate(path):
                if pi<p_len-1:
                    temp+='%s -> '%pat
                else:
                    temp += '%s' % pat
            print(temp)



if __name__ == "__main__":
    # testing
    g=CreateGraph()
    g.add_vertices(1,2)
    g.add_vertices(1,3)
    g.add_vertices(1,4)
    g.add_vertices(1,5)
    g.add_vertices(2,6)
    g.add_vertices(3,6)
    g.add_vertices(3,7)
    g.add_vertices(4,7)
    g.add_vertices(4,8)
    g.add_vertices(5,8)
    # g.remove_verticies(2,remove_with_links=True )
    graph=g.get_graph()

    c=DecodeGraph(graph)
    c.print_paths()