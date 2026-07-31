import streamlit as st
import pandas as pd
import heapq

st.set_page_config(page_title="Dijkstra's Algorithm", page_icon="🛣️")

st.title("🛣️ Dijkstra's Shortest Path Algorithm")
st.write("Find the shortest path from a selected source vertex using **Dijkstra's Algorithm**.")

# ---------------- Dijkstra Algorithm ---------------- #

def dijkstra(graph, source):

    n = len(graph)

    dist = [float("inf")] * n
    prev = [None] * n

    dist[source] = 0

    pq = [(0, source)]
    visited = set()

    while pq:

        current_distance, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, weight in graph[u]:

            if dist[u] + weight < dist[v]:

                dist[v] = dist[u] + weight
                prev[v] = u

                heapq.heappush(pq, (dist[v], v))

    return dist, prev


# ---------------- Path Reconstruction ---------------- #

def reconstruct_path(prev, source, target):

    path = []

    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path

    return []


# ---------------- Graph ---------------- #

graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

# ---------------- Display Graph ---------------- #

st.subheader("Graph Edges")

edges = []

for u in graph:
    for v, w in graph[u]:
        edges.append({
            "Source": u,
            "Destination": v,
            "Weight": w
        })

st.table(pd.DataFrame(edges))

# ---------------- Source Vertex ---------------- #

source = st.selectbox(
    "Select Source Vertex",
    list(graph.keys()),
    index=0
)

# ---------------- Run Algorithm ---------------- #

if st.button("Find Shortest Paths"):

    dist, prev = dijkstra(graph, source)

    result = []

    for vertex in range(len(graph)):

        path = reconstruct_path(prev, source, vertex)

        if path:
            path_str = " → ".join(map(str, path))
        else:
            path_str = "No Path"

        distance = dist[vertex]

        if distance == float("inf"):
            distance = "INF"

        result.append({
            "Vertex": vertex,
            "Distance": distance,
            "Path": path_str
        })

    st.subheader("Shortest Paths")

    st.table(pd.DataFrame(result))

    st.success("Shortest paths calculated successfully.")
