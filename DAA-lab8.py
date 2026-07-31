import streamlit as st
import pandas as pd
from itertools import permutations

st.set_page_config(page_title="Travelling Salesman Problem", page_icon="🗺️")

st.title("🗺️ Travelling Salesman Problem (TSP)")
st.subheader("Brute Force Approach")

INF = float('inf')

# ------------------ TSP Algorithm ------------------ #

def tsp_brute_force(cost, n):
    cities = list(range(1, n))

    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]

        total_cost = 0

        for i in range(n):
            total_cost += cost[path[i]][path[i + 1]]

        if total_cost < best_cost:
            best_cost = total_cost
            best_path = path

    return best_path, best_cost


# ------------------ Cost Matrix ------------------ #

cities = ["A", "B", "C", "D", "E"]

cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

n = len(cost)

# ------------------ Display Matrix ------------------ #

st.subheader("Cost Matrix")

display_matrix = []

for row in cost:
    display_matrix.append(
        ["INF" if x == INF else x for x in row]
    )

df = pd.DataFrame(display_matrix, columns=cities, index=cities)

st.table(df)

# ------------------ Solve Button ------------------ #

if st.button("Find Optimal Tour"):

    best_path, best_cost = tsp_brute_force(cost, n)

    tour = " → ".join(cities[i] for i in best_path)

    st.success(f"Optimal Tour : {tour}")

    st.success(f"Minimum Cost : {best_cost}")

    st.subheader("Path Verification")

    verification = []

    total = 0

    for i in range(n):

        u = best_path[i]
        v = best_path[i + 1]

        edge_cost = cost[u][v]

        total += edge_cost

        verification.append({
            "From": cities[u],
            "To": cities[v],
            "Cost": edge_cost
        })

    st.table(pd.DataFrame(verification))

    st.info(f"Total Cost = {total}")
 
