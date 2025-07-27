"""Minimal stub of NetworkX for environments without the real package.

This module provides a subset of the NetworkX API required by the ULTIMAI
reasoning infrastructure.  It includes a simple directed graph class and
implementations of a few common algorithms.  The goal is not to match
NetworkX's full functionality or performance, but to supply enough
capability for local unit tests and basic metrics without external
dependencies.

Implemented features:
  - ``DiGraph`` class with methods ``add_node``, ``add_edge``, ``nodes``,
    ``edges``, ``has_node``, ``has_edge``, ``get_edge_data``, ``degree``,
    ``out_degree``, ``in_degree``, ``neighbors``, ``number_of_nodes``,
    ``number_of_edges``, and ``subgraph``.
  - ``degree_centrality`` computes normalised degree centrality.
  - ``betweenness_centrality`` returns zeros for all nodes (placeholder).
  - ``pagerank`` returns a uniform distribution over nodes.
  - ``node_link_data`` and ``node_link_graph`` provide simple serialisation.
  - ``shortest_path`` performs a BFS to find one shortest path.
  - Exception classes ``NetworkXNoPath`` and ``NodeNotFound`` mimic
    NetworkX behaviour for path finding errors.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple


class NetworkXNoPath(Exception):
    """Raised when no path exists between two nodes."""


class NodeNotFound(Exception):
    """Raised when a requested node is not present in the graph."""


class NodeView:
    """A view of the graph's nodes supporting len, membership and indexing."""

    def __init__(self, graph: 'DiGraph') -> None:
        self._graph = graph

    def __iter__(self) -> Iterator[Any]:
        return iter(self._graph._nodes)

    def __len__(self) -> int:
        return len(self._graph._nodes)

    def __contains__(self, node: Any) -> bool:
        return node in self._graph._nodes

    def __getitem__(self, node: Any) -> Dict[str, Any]:
        return self._graph._nodes[node]

    def __call__(self, data: bool = False) -> Iterable[Any | Tuple[Any, Dict[str, Any]]]:
        """Allow the view to be called like ``graph.nodes(data=True)``."""
        return self._graph.nodes_iter(data=data)


class EdgeView:
    """A view of the graph's edges supporting len and iteration."""

    def __init__(self, graph: 'DiGraph') -> None:
        self._graph = graph

    def __iter__(self) -> Iterator[Any]:
        for u in self._graph._adj:
            for v in self._graph._adj[u]:
                yield (u, v)

    def __len__(self) -> int:
        return self._graph.number_of_edges()

    def __call__(self, data: bool = False) -> Iterable[Tuple[Any, Any] | Tuple[Any, Any, Dict[str, Any]]]:
        """Allow the view to be called like ``graph.edges(data=True)``."""
        return self._graph.edges_iter(data=data)


class DiGraph:
    """A simple directed graph implementation."""

    def __init__(self) -> None:
        self._nodes: Dict[Any, Dict[str, Any]] = {}
        # adjacency list: node -> {successor: edge_attributes}
        self._adj: Dict[Any, Dict[Any, Dict[str, Any]]] = {}
        # predecessor list: node -> {predecessor: edge_attributes}
        self._pred: Dict[Any, Dict[Any, Dict[str, Any]]] = {}
        # views will be provided via properties

    # Node operations
    def add_node(self, node: Any, **attrs: Any) -> None:
        if node not in self._nodes:
            self._nodes[node] = {}
            self._adj[node] = {}
            self._pred[node] = {}
        # update attributes
        self._nodes[node].update(attrs)

    def has_node(self, node: Any) -> bool:
        return node in self._nodes

    # Edge operations
    def add_edge(self, u: Any, v: Any, **attrs: Any) -> None:
        if u not in self._nodes:
            self.add_node(u)
        if v not in self._nodes:
            self.add_node(v)
        self._adj[u][v] = attrs.copy()
        self._pred[v][u] = attrs.copy()

    def has_edge(self, u: Any, v: Any) -> bool:
        return v in self._adj.get(u, {})

    def get_edge_data(self, u: Any, v: Any) -> Optional[Dict[str, Any]]:
        return self._adj.get(u, {}).get(v)

    # Accessors
    def nodes_iter(self, data: bool = False) -> Iterable[Any | Tuple[Any, Dict[str, Any]]]:
        """Return an iterable of node identifiers or (id, attrs) tuples."""
        if data:
            return [(n, self._nodes[n].copy()) for n in self._nodes]
        return list(self._nodes.keys())

    def edges_iter(self, data: bool = False) -> Iterable[Tuple[Any, Any] | Tuple[Any, Any, Dict[str, Any]]]:
        """Return an iterable of edges as tuples (u, v[, attrs])."""
        for u, nbrs in self._adj.items():
            for v, attrs in nbrs.items():
                yield (u, v, attrs.copy()) if data else (u, v)

    @property
    def nodes(self) -> NodeView:
        """Return a dynamic view over the graph's nodes."""
        return NodeView(self)

    @property
    def edges(self) -> EdgeView:
        """Return a dynamic view over the graph's edges."""
        return EdgeView(self)

    def degree(self) -> Iterable[Tuple[Any, int]]:
        for n in self._nodes:
            deg = len(self._adj[n]) + len(self._pred[n])
            yield (n, deg)

    def out_degree(self, n: Any) -> int:
        return len(self._adj.get(n, {}))

    def in_degree(self, n: Any) -> int:
        return len(self._pred.get(n, {}))

    def neighbors(self, n: Any) -> List[Any]:
        return list(self._adj.get(n, {}).keys())

    def number_of_nodes(self) -> int:
        return len(self._nodes)

    def number_of_edges(self) -> int:
        return sum(len(adj) for adj in self._adj.values())

    def subgraph(self, nodes: Iterable[Any]) -> 'DiGraph':
        sg = DiGraph()
        node_set = set(nodes)
        for n in node_set:
            if n in self._nodes:
                sg.add_node(n, **self._nodes[n])
        for u in node_set:
            for v, attrs in self._adj.get(u, {}).items():
                if v in node_set:
                    sg.add_edge(u, v, **attrs)
        return sg

    # Node attribute access
    @property
    def nodes_attr(self) -> Dict[Any, Dict[str, Any]]:
        """Return direct access to the node attributes dictionary."""
        return self._nodes

    @property
    def adj(self) -> Dict[Any, Dict[Any, Dict[str, Any]]]:
        return self._adj

    @property
    def pred(self) -> Dict[Any, Dict[Any, Dict[str, Any]]]:
        return self._pred


def degree_centrality(g: DiGraph) -> Dict[Any, float]:
    """Return a simple degree-based centrality for a directed graph.

    Unlike the classic NetworkX definition, this implementation scales
    node centrality scores such that their sum equals the number of
    nodes.  Each score is proportional to the node's total degree
    (in_degree + out_degree) relative to the total degree of all
    nodes.  If the graph is empty or contains a single node, a zero
    vector is returned.
    """
    n = g.number_of_nodes()
    if n <= 1:
        return {node: 0.0 for node in g.nodes()}
    # Compute total degree for each node and the sum of all degrees
    degrees = {node: deg for node, deg in g.degree()}
    total_deg = sum(degrees.values())
    if total_deg == 0:
        # No edges: distribute scores uniformly
        return {node: 1.0 for node in g.nodes()}
    # Scale degrees so that the sum of scores equals n
    return {node: (deg / total_deg) * n for node, deg in degrees.items()}


def betweenness_centrality(g: DiGraph) -> Dict[Any, float]:
    """Return betweenness centrality (placeholder returning zeros)."""
    return {node: 0.0 for node in g.nodes()}


def pagerank(g: DiGraph, alpha: float = 0.85) -> Dict[Any, float]:
    """Return a simple PageRank vector assigning equal weight to all nodes."""
    n = g.number_of_nodes()
    if n == 0:
        return {}
    weight = 1.0 / n
    return {node: weight for node in g.nodes()}


def node_link_data(g: DiGraph) -> Dict[str, Any]:
    """Return a node-link representation of the graph."""
    # Copy nodes with attributes
    nodes = [dict(id=n, **g._nodes[n]) for n in g._nodes]
    # Copy edges with attributes
    links = []
    for u in g._adj:
        for v, attrs in g._adj[u].items():
            link = dict(source=u, target=v)
            link.update(attrs)
            links.append(link)
    return {"directed": True, "multigraph": False, "graph": {}, "nodes": nodes, "links": links}


def node_link_graph(data: Dict[str, Any]) -> DiGraph:
    """Create a graph from node-link data."""
    g = DiGraph()
    for node in data.get("nodes", []):
        nid = node.get("id")
        if nid is None:
            continue
        attrs = {k: v for k, v in node.items() if k != "id"}
        g.add_node(nid, **attrs)
    for link in data.get("links", []):
        u = link.get("source")
        v = link.get("target")
        if u is not None and v is not None:
            attrs = {k: v for k, v in link.items() if k not in ("source", "target")}
            g.add_edge(u, v, **attrs)
    return g


def shortest_path(g: DiGraph, source: Any, target: Any) -> List[Any]:
    """Return one shortest path from source to target using BFS.

    Raises NodeNotFound if source or target is missing, NetworkXNoPath if no
    path exists.
    """
    if source not in g._nodes:
        raise NodeNotFound(f"Node {source!r} not found in graph")
    if target not in g._nodes:
        raise NodeNotFound(f"Node {target!r} not found in graph")
    if source == target:
        return [source]
    # BFS
    queue: deque[Any] = deque([source])
    parents: Dict[Any, Any] = {source: None}
    found = False
    while queue and not found:
        u = queue.popleft()
        for v in g.neighbors(u):
            if v not in parents:
                parents[v] = u
                if v == target:
                    found = True
                    break
                queue.append(v)
    if not found:
        raise NetworkXNoPath(f"No path between {source!r} and {target!r}")
    # reconstruct path
    path: List[Any] = [target]
    while parents[path[-1]] is not None:
        path.append(parents[path[-1]])
    path.reverse()
    return path


# Provide alias to match networkx's interface
class exceptions:
    NetworkXNoPath = NetworkXNoPath  # type: ignore
    NodeNotFound = NodeNotFound  # type: ignore
