from collections import deque
from typing import Dict, Set, Optional, List


Graph = Dict[int, Set[int]]


def connect(graph: Graph, vertex: int, other: int) -> None:
    graph[vertex].add(other)
    graph[other].add(vertex)


def shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
    """
    Find the shortest path in a undirected Graph
    :return: The list of vertices from start to end.
        Empty list if the path doesn't exist
    """
    to_process = deque()
    to_process.append(start)
    predecessors = {start: start}
    while to_process:
        node = to_process.popleft()
        if node == end:
            break
        for neighbor in graph[node]:
            if neighbor in predecessors:
                continue
            to_process.append(neighbor)
            predecessors[neighbor] = node
    if end not in predecessors:
        return None
    path = [end]
    back = end
    while back != start:
        back = predecessors[back]
        path.append(back)
    return path[::-1]
