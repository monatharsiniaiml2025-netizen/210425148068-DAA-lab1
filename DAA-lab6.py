import streamlit as st
import pandas as pd

st.set_page_config(page_title="Matrix Chain Multiplication", page_icon="📊")

st.title("📊 Matrix Chain Multiplication using Dynamic Programming")

st.write("""
Enter the dimensions of the matrices.

Example:
- A1 = 10 × 30
- A2 = 30 × 5
- A3 = 5 × 60
- A4 = 60 × 10

Dimensions should be entered as:
**10,30,5,60,10**
""")

# ---------------- Matrix Chain Algorithm ---------------- #

def matrix_chain_order(dims):
    n = len(dims) - 1

    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')

            for k in range(i, j):
                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# ---------------- User Input ---------------- #

dimension_input = st.text_input(
    "Enter Matrix Dimensions",
    "10,30,5,60,10"
)

if st.button("Find Optimal Order"):

    try:
        dims = [int(x.strip()) for x in dimension_input.split(",")]

        if len(dims) < 2:
            st.error("Please enter at least two dimensions.")
        else:

            n = len(dims) - 1

            st.subheader("Matrix Dimensions")

            matrix_data = []

            for i in range(n):
                matrix_data.append({
                    "Matrix": f"A{i+1}",
                    "Dimension": f"{dims[i]} × {dims[i+1]}"
                })

            st.table(pd.DataFrame(matrix_data))

            # DP
            m, s = matrix_chain_order(dims)

            st.success(
                f"Minimum Scalar Multiplications = {m[1][n]}"
            )

            st.info(
                f"Optimal Parenthesization: {print_optimal_parens(s,1,n)}"
            )

            # DP Table
            st.subheader("DP Cost Table")

            table = []

            headers = [f"A{i}" for i in range(1, n + 1)]

            for i in range(1, n + 1):

                row = []

                for j in range(1, n + 1):

                    if j < i:
                        row.append("---")
                    else:
                        row.append(m[i][j])

                table.append(row)

            df = pd.DataFrame(table, columns=headers)
            df.index = headers

            st.table(df)

    except ValueError:
        st.error("Please enter valid integers separated by commas.")
 
