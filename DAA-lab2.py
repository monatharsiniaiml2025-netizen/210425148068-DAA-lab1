import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="String Pattern Matching", page_icon="🔍")

st.title("🔍 String Pattern Matching Algorithms")
st.write("Compare **Naive Search**, **KMP**, and **Rabin-Karp** algorithms.")

# ---------------- Naive Search ---------------- #

def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)

    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons


# ---------------- KMP ---------------- #

def compute_lps(pattern):
    m = len(pattern)

    lps = [0] * m

    length = 0
    i = 1

    while i < m:

        if pattern[i] == pattern[length]:

            length += 1
            lps[i] = length
            i += 1

        elif length != 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):

    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:

        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and pattern[j] != text[i]:

            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


# ---------------- Rabin-Karp ---------------- #

def rabin_karp(text, pattern, q=101):

    n = len(text)
    m = len(pattern)

    d = 256

    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:

            for k in range(m):

                comparisons += 1

                if text[s + k] != pattern[k]:
                    break

            else:
                matches.append(s)

        if s < n - m:

            t_hash = (
                d * (t_hash - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# ---------------- User Input ---------------- #

st.header("Search Pattern")

text = st.text_input(
    "Enter Text",
    "AABAACAADAABAABA"
)

pattern = st.text_input(
    "Enter Pattern",
    "AABA"
)

if st.button("Search"):

    m1, c1 = naive_search(text, pattern)
    m2, c2 = kmp_search(text, pattern)
    m3, c3 = rabin_karp(text, pattern)

    result = pd.DataFrame({
        "Algorithm": [
            "Naive",
            "KMP",
            "Rabin-Karp"
        ],
        "Match Positions": [
            str(m1),
            str(m2),
            str(m3)
        ],
        "Comparisons": [
            c1,
            c2,
            c3
        ]
    })

    st.subheader("Search Result")

    st.table(result)


# ---------------- Performance Analysis ---------------- #

st.header("Performance Comparison")

if st.button("Run Performance Test"):

    text_large = ''.join(random.choices("ABCD", k=10000))

    patterns = [
        "AB",
        "ABCD",
        "ABCDAB",
        "ABCDABCD"
    ]

    results = []

    for p in patterns:

        _, c1 = naive_search(text_large, p)
        _, c2 = kmp_search(text_large, p)
        _, c3 = rabin_karp(text_large, p)

        results.append({
            "Pattern": p,
            "Naive": c1,
            "KMP": c2,
            "Rabin-Karp": c3
        })

    st.subheader("Comparison Table")

    st.table(pd.DataFrame(results))

    st.subheader("Observation")

    st.write("""
- **Naive Search** checks every possible position and is simple to implement.
- **KMP** avoids unnecessary comparisons using the **LPS (Longest Prefix Suffix)** array.
- **Rabin-Karp** uses hashing, making it efficient for searching multiple patterns.
- For large texts, **KMP** generally performs the fewest comparisons.
""")
 
