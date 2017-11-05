# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~
    stuff.graph_isolator
    Find all isolated graphs from set of edges.
    ~~~~~~~~~~~~~~~~
    :copyright: (c) 2017 by Stas Kazhavets.
"""
from itertools import chain, count


def get_number_generator():
    """Creates sequential numbers generator."""
    counter = count()

    def get_uniq_graph_id():
        return next(counter)
    return get_uniq_graph_id


class GraphIsolator(object):
    """Implements naive algorithm to build a list of isolated
    graphs from list of edges.
    """
    def __init__(self):
        self.graphs = {}
        self.united_graphs = set()
        self.vertex_index = {}
        self.seq_gen = get_number_generator()

    def get_graphs(self):
        return self.graphs.values()

    def add_edge(self, edge):
        """Add edge in form `(a, b)` where `a` and `b` are vertexes."""
        left, right = edge

        left_graph_index = self.vertex_index.get(left)
        right_graph_index = self.vertex_index.get(right)

        if left_graph_index is None and right_graph_index is None:
            # edge's vertexes are not in any existing graph
            # add new slots in vertex_index and graphs
            new_graph = [edge]
            graph_no = self.seq_gen()

            self.vertex_index[left] = graph_no
            self.vertex_index[right] = graph_no
            self.graphs[graph_no] = new_graph

        elif left_graph_index is not None and right_graph_index is not None:
            # both edges are in existing graphs
            # check if it is the same graph
            if left_graph_index == right_graph_index:
                # do nothing, edge already in graph with index == left_graph_index.
                return

            # each vertex in separate graph - union them:
            # optional
            min_index, max_index = sorted([left_graph_index, right_graph_index])

            # get graph with biggest index
            graph_to_be_merged = self.graphs[max_index]
            graph_to_merge_in = self.graphs[min_index]

            # actual merge
            graph_to_merge_in.extend(graph_to_be_merged)
            self.united_graphs.add(min_index)

            # update all merged edges in vertex_index
            merged_vertexes = chain.from_iterable(graph_to_be_merged)
            for vertex in merged_vertexes:
                self.vertex_index[vertex] = min_index

            # delete merged graph from known graphs
            del self.graphs[max_index]
            self.united_graphs.discard(max_index)

            # finally add new edge to the graph with minimal seq_no
            # since both vertexes were already in vertex_index and merged
            # vertexes were updated there are no need to update edge's vertexes in vertex_index.
            graph_to_merge_in.append(edge)
        else:
            # get_target graph index
            target_graph_index = (left_graph_index if left_graph_index is not None
                                  else right_graph_index)
            free_vertex = left if left_graph_index is None else right

            # add edge to targeted graph
            self.graphs[target_graph_index].append(edge)

            # add free vertex to edge_index
            self.vertex_index[free_vertex] = target_graph_index
