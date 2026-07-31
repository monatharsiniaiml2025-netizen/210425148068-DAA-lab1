import streamlit as st
import pandas as pd
import heapq

st.set_page_config(page_title="Minimum Spanning Tree", page_icon="🌳")

st.title("🌳 Minimum Spanning Tree (MST)")
st.write("Compare **Kruskal's Algorithm** and **Prim's Algorithm**.")

# ---------------- Union Find ---------------- #

class UnionFind:

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x, y):

        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# ---------------- Kruskal ---------------- #

def kruskal(n, edges):

    edges = sorted(edges)

    uf = UnionFind(n)

    mst = []
    total_cost = 0

    for w, u, v in edges:

        if uf.union(u, v):

            mst.append((u, v, w))
            total_cost += w

            if len(mst) == n - 1:
                break

    return mst, total_cost


# ---------------- Prim ---------------- #

def prim(n, adj, start=0):

    INF = float("inf")

    key = [INF] * n
    parent = [-1] * n
    in_mst = [False] * n

    key[start] = 0

    pq = [(0, start)]

    mst = []
    total_cost = 0

    while pq:

        weight, u = heapq.heappop(pq)

        if in_mst[u]:
            continue

        in_mst[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, weight))
            total_cost += weight

        for v, wt in adj.get(u, []):

            if not in_mst[v] and wt < key[v]:

                key[v] = wt
                parent[v] = u

                heapq.heappush(pq, (wt, v))

    return mst, total_cost


# ---------------- Graph ---------------- #

n = 7

edges = [
    (7, 0, 1),
    (5, 0, 3),
    (8, 1, 2),
    (9, 1, 3),
    (7, 1, 4),
    (5, 2, 4),
    (15, 3, 4),
    (6, 3, 5),
    (8, 4, 5),
    (9, 4, 6),
    (11, 5, 6)
]

adj = {}

for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))


# ---------------- Display Graph ---------------- #

st.subheader("Graph Edges")

graph_df = pd.DataFrame(
    {
        "Source": [u for _, u, _ in edges],
        "Destination": [v for _, _, v in edges],
        "Weight": [w for w, _, _ in edges],
    }
)

st.table(graph_df)


# ---------------- Find MST ---------------- #

if st.button("Find MST"):

    k_mst, k_cost = kruskal(n, edges.copy())

    p_mst, p_cost = prim(n, adj)

    st.subheader("Kruskal's MST")

    k_df = pd.DataFrame(
        {
            "Source": [u for u, v, w in k_mst],
            "Destination": [v for u, v, w in k_mst],
            "Weight": [w for u, v, w in k_mst],
        }
    )

    st.table(k_df)

    st.success(f"Total MST Cost = {k_cost}")

    st.subheader("Prim's MST")

    p_df = pd.DataFrame(
        {
            "Source": [u for u, v, w in p_mst],
            "Destination": [v for u, v, w in p_mst],
            "Weight": [w for u, v, w in p_mst],
        }
    )

    st.table(p_df)

    st.success(f"Total MST Cost = {p_cost}")

    if k_cost == p_cost:
        st.info("✅ Both Kruskal's and Prim's algorithms produce the same Minimum Spanning Tree cost.")
