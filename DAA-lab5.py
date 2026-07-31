import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Min-Max using Divide & Conquer", page_icon="📊")

st.title("📊 Min-Max using Divide & Conquer")
st.write("Compare Divide & Conquer with the Naive approach.")

# Global comparison counter
comparison_count = 0


def min_max_dc(arr, low, high):
    global comparison_count

    # Base case: Single element
    if low == high:
        return arr[low], arr[low]

    # Base case: Two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2

    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Conquer
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin

    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    mn = mx = arr[0]
    comps = 0

    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x

        comps += 1
        if x > mx:
            mx = x

    return mn, mx, comps


st.header("Demo with Sample Array")

sample_array = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]

if st.button("Run Demo"):

    comparison_count = 0
    mn, mx = min_max_dc(sample_array, 0, len(sample_array) - 1)
    dc_comps = comparison_count

    _, _, naive_comps = min_max_naive(sample_array)

    st.write("### Sample Array")
    st.write(sample_array)

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"Minimum = {mn}")

    with col2:
        st.success(f"Maximum = {mx}")

    st.info(f"Divide & Conquer Comparisons: **{dc_comps}**")
    st.info(f"Naive Comparisons: **{naive_comps}**")


st.header("Performance Analysis")

sizes = [10, 100, 1000, 10000]

if st.button("Analyze Performance"):

    results = []

    for size in sizes:

        arr = [random.randint(1, 10000) for _ in range(size)]

        comparison_count = 0
        mn, mx = min_max_dc(arr, 0, len(arr) - 1)
        dc = comparison_count

        _, _, naive = min_max_naive(arr)

        formula = 3 * size // 2 - 2

        results.append({
            "Array Size": size,
            "D&C Comparisons": dc,
            "Naive Comparisons": naive,
            "Formula (3n/2 - 2)": formula
        })

    df = pd.DataFrame(results)

    st.table(df)

    st.subheader("Observation")

    st.write("""
- Divide & Conquer requires fewer comparisons than the Naive approach.
- Naive Approach performs approximately **2(n−1)** comparisons.
- Divide & Conquer performs approximately **3n/2 − 2** comparisons.
- As the input size increases, Divide & Conquer becomes more efficient.
""")
