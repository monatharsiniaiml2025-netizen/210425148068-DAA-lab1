import streamlit as st

st.set_page_config(page_title="N-Queens Solver", page_icon="♛")

st.title("♛ N-Queens Problem using Backtracking")

st.write("""
This application solves the **N-Queens Problem** using the **Backtracking Algorithm**.

- Displays **all solutions** for the selected value of **N**.
- Shows the **number of solutions**.
- Shows the **number of backtracks**.
""")


# ------------------ Algorithm ------------------ #

def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]

        # Same column
        if placed == col:
            return False

        # Same diagonal
        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


def solve_n_queens(n):

    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):

        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):

            if is_safe(board, row, col):

                board[row] = col

                backtrack(row + 1)

                board[row] = -1
                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


# ---------------- Display Board ---------------- #

def board_to_string(solution, n):

    board = ""

    border = "+" + "---+" * n + "\n"

    board += border

    for row in range(n):

        board += "|"

        for col in range(n):

            if solution[row] == col:
                board += " Q |"
            else:
                board += " . |"

        board += "\n"
        board += border

    return board


# ---------------- UI ---------------- #

n = st.selectbox(
    "Select the value of N",
    [4, 5, 6, 7, 8],
    index=0
)

if st.button("Solve"):

    solutions, backtracks = solve_n_queens(n)

    st.success(f"Number of Solutions : {len(solutions)}")

    st.info(f"Number of Backtracks : {backtracks}")

    st.subheader("Solutions")

    if len(solutions) == 0:
        st.warning("No solution exists.")

    else:

        for i, sol in enumerate(solutions, start=1):

            st.markdown(f"### Solution {i}")

            st.write(sol)

            st.code(board_to_string(sol, n))
