import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Travelling Salesman Problem",
    page_icon="🗺️"
)

st.title("🗺️ Travelling Salesman Problem (TSP)")
st.subheader("Branch and Bound Approach")

INF = float('inf')


# ------------------ Branch and Bound TSP Algorithm ------------------

def tsp_branch_and_bound(cost, n):

    final_path = [-1] * (n + 1)
    visited = [False] * n

    # Start from city 0
    visited[0] = True
    current_path = [0]

    # Find the first minimum edge for a city
    def first_min(i):
        minimum = INF

        for k in range(n):
            if i != k and cost[i][k] < minimum:
                minimum = cost[i][k]

        return minimum

    # Find the second minimum edge for a city
    def second_min(i):
        first = INF
        second = INF

        for j in range(n):
            if i == j:
                continue

            if cost[i][j] <= first:
                second = first
                first = cost[i][j]

            elif cost[i][j] < second:
                second = cost[i][j]

        return second

    # Initial lower bound
    initial_bound = 0

    for i in range(n):
        initial_bound += first_min(i) + second_min(i)

    initial_bound = initial_bound / 2

    best_cost = [INF]
    best_path = [None]

    # Branch and Bound recursive function
    def branch_and_bound(current_bound, current_cost, level):

        # If all cities are visited
        if level == n:

            last_city = current_path[-1]

            # Check if we can return to starting city
            if cost[last_city][0] != INF:

                total_cost = (
                    current_cost +
                    cost[last_city][0]
                )

                if total_cost < best_cost[0]:

                    best_cost[0] = total_cost

                    best_path[0] = (
                        current_path.copy() + [0]
                    )

            return

        # Try every unvisited city
        for next_city in range(1, n):

            current_city = current_path[-1]

            if (
                not visited[next_city]
                and cost[current_city][next_city] != INF
            ):

                new_cost = (
                    current_cost +
                    cost[current_city][next_city]
                )

                # Calculate new lower bound
                if level == 1:

                    new_bound = (
                        current_bound -
                        (
                            first_min(current_city)
                            + first_min(next_city)
                        ) / 2
                    )

                else:

                    new_bound = (
                        current_bound -
                        (
                            second_min(current_city)
                            + first_min(next_city)
                        ) / 2
                    )

                # Continue only if promising
                if new_cost + new_bound < best_cost[0]:

                    visited[next_city] = True
                    current_path.append(next_city)

                    branch_and_bound(
                        new_bound,
                        new_cost,
                        level + 1
                    )

                    # Backtracking
                    current_path.pop()
                    visited[next_city] = False

    branch_and_bound(
        initial_bound,
        0,
        1
    )

    return best_path[0], best_cost[0]


# ------------------ Cost Matrix ------------------

cities = ["A", "B", "C", "D", "E"]

cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

n = len(cost)


# ------------------ Display Matrix ------------------

st.subheader("Cost Matrix")

display_matrix = []

for row in cost:
    display_matrix.append(
        ["INF" if x == INF else x for x in row]
    )

df = pd.DataFrame(
    display_matrix,
    columns=cities,
    index=cities
)

st.table(df)


# ------------------ Solve Button ------------------

if st.button("Find Optimal Tour"):

    best_path, best_cost = tsp_branch_and_bound(
        cost,
        n
    )

    if best_path is not None:

        # Convert city numbers to city names
        tour = " → ".join(
            cities[i] for i in best_path
        )

        st.success(
            f"Optimal Tour : {tour}"
        )

        st.success(
            f"Minimum Cost : {best_cost}"
        )

        # ------------------ Path Verification ------------------

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

        st.table(
            pd.DataFrame(verification)
        )

        st.info(
            f"Total Cost = {total}"
        )
 
