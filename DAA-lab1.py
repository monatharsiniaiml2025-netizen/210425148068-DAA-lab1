import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Interpolation Search", page_icon="🔍")

st.title("🔍 Interpolation Search vs Binary Search")
st.write("Compare the performance of **Interpolation Search** and **Binary Search**.")

# ---------------- Interpolation Search ---------------- #

def interpolation_search(arr, target):
    low = 0
    high = len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:

        comparisons += 1

        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        if arr[high] == arr[low]:
            break

        pos = low + int(
            ((target - arr[low]) * (high - low))
            / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos, comparisons

        elif arr[pos] < target:
            low = pos + 1

        else:
            high = pos - 1

    return -1, comparisons


# ---------------- Binary Search ---------------- #

def binary_search(arr, target):

    low = 0
    high = len(arr) - 1
    comparisons = 0

    while low <= high:

        comparisons += 1

        mid = (low + high) // 2

        if arr[mid] == target:
            return mid, comparisons

        elif arr[mid] < target:
            low = mid + 1

        else:
            high = mid - 1

    return -1, comparisons


# ---------------- Sample Search ---------------- #

st.header("Sample Search")

sample_array = [2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120]

target = st.number_input(
    "Enter Target",
    min_value=min(sample_array),
    max_value=max(sample_array),
    value=35
)

st.write("Array:")
st.code(sample_array)

if st.button("Search"):

    idx, comps = interpolation_search(sample_array, target)

    if idx != -1:
        st.success(f"Target found at Index {idx}")
    else:
        st.error("Target not found")

    st.info(f"Interpolation Search Comparisons : {comps}")


# ---------------- Performance Analysis ---------------- #

st.header("Performance Analysis")

if st.button("Run Performance Test"):

    sizes = [1000, 5000, 10000, 50000, 100000]

    results = []

    for size in sizes:

        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        # Interpolation Search

        start = time.perf_counter()

        for _ in range(100):
            _, comp_is = interpolation_search(arr, target)

        is_time = (time.perf_counter() - start) / 100 * 1000

        # Binary Search

        start = time.perf_counter()

        for _ in range(100):
            _, comp_bs = binary_search(arr, target)

        bs_time = (time.perf_counter() - start) / 100 * 1000

        results.append({
            "Array Size": size,
            "IS Time (ms)": round(is_time, 4),
            "BS Time (ms)": round(bs_time, 4),
            "IS Comparisons": comp_is,
            "BS Comparisons": comp_bs
        })

    df = pd.DataFrame(results)

    st.subheader("Performance Comparison")
    st.table(df)

    st.subheader("Observation")

    st.write("""
- **Interpolation Search** performs best on **uniformly distributed sorted data**.
- **Binary Search** performs consistently on all sorted datasets.
- Interpolation Search often uses **fewer comparisons** for uniformly distributed values.
- Binary Search guarantees **O(log n)** time complexity.
""")
