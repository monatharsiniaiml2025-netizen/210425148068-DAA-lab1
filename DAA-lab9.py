import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Bin Packing Problem", page_icon="📦")

st.title("📦 Bin Packing Problem")
st.write("Compare **First Fit (FF)**, **First Fit Decreasing (FFD)** and **Best Fit Decreasing (BFD)** algorithms.")

# ---------------- First Fit ---------------- #

def first_fit(items, capacity=1.0):

    bins = []
    bin_contents = []

    for item in items:

        placed = False

        for i, space in enumerate(bins):

            if space >= item:

                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:

            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------- First Fit Decreasing ---------------- #

def first_fit_decreasing(items, capacity=1.0):

    return first_fit(sorted(items, reverse=True), capacity)


# ---------------- Best Fit Decreasing ---------------- #

def best_fit_decreasing(items, capacity=1.0):

    items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in items:

        best_index = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            if space >= item and (space - item) < best_space:

                best_space = space - item
                best_index = i

        if best_index != -1:

            bins[best_index] -= item
            bin_contents[best_index].append(item)

        else:

            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------- Display Function ---------------- #

def display_bins(title, bins):

    st.subheader(f"{title} ({len(bins)} Bins)")

    data = []

    for i, b in enumerate(bins):

        used = round(sum(b), 2)
        remaining = round(1.0 - used, 2)

        data.append({
            "Bin": f"Bin {i+1}",
            "Items": str([round(x,1) for x in b]),
            "Used Space": used,
            "Remaining Space": remaining
        })

    st.table(pd.DataFrame(data))


# ---------------- Input ---------------- #

default_items = "0.5,0.7,0.3,0.9,0.2,0.6,0.8,0.4,0.1,0.5"

item_input = st.text_input(
    "Enter Item Sizes (comma separated)",
    default_items
)

capacity = st.number_input(
    "Bin Capacity",
    value=1.0,
    step=0.1
)

# ---------------- Solve ---------------- #

if st.button("Run Bin Packing"):

    try:

        items = [float(x.strip()) for x in item_input.split(",")]

        lower_bound = math.ceil(sum(items) / capacity)

        st.write("### Input")

        st.write(f"Items : {items}")
        st.write(f"Capacity : {capacity}")
        st.write(f"Total Size : {round(sum(items),2)}")
        st.success(f"Lower Bound on Bins : {lower_bound}")

        ff = first_fit(items, capacity)
        ffd = first_fit_decreasing(items, capacity)
        bfd = best_fit_decreasing(items, capacity)

        display_bins("First Fit (FF)", ff)
        display_bins("First Fit Decreasing (FFD)", ffd)
        display_bins("Best Fit Decreasing (BFD)", bfd)

        st.subheader("Summary")

        summary = pd.DataFrame({
            "Algorithm": [
                "Lower Bound",
                "First Fit",
                "First Fit Decreasing",
                "Best Fit Decreasing"
            ],
            "Number of Bins": [
                lower_bound,
                len(ff),
                len(ffd),
                len(bfd)
            ]
        })

        st.table(summary)

    except:
        st.error("Please enter valid decimal values separated by commas.")
