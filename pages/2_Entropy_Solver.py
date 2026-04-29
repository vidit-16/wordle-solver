import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Hybrid Solver", page_icon="🤖")

st.title("🤖 Wordle Solver (Hybrid)")

# -----------------------------
# Load
# -----------------------------
@st.cache_data
def load_lists():
    g = pd.read_csv("valid_guesses.csv")
    s = pd.read_csv("valid_solutions.csv")

    guesses = g["word"].dropna().str.upper().tolist()
    solutions = s["word"].dropna().str.upper().tolist()

    guesses = [w for w in guesses if len(w) == 5 and w.isalpha()]
    solutions = [w for w in solutions if len(w) == 5 and w.isalpha()]

    return guesses, solutions

# -----------------------------
# Feedback
# -----------------------------
def feedback(guess, target):
    pattern = [''] * 5
    target_chars = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            pattern[i] = 'G'
            target_chars[i] = None

    for i in range(5):
        if pattern[i] == '':
            if guess[i] in target_chars:
                pattern[i] = 'Y'
                target_chars[target_chars.index(guess[i])] = None
            else:
                pattern[i] = 'B'

    return ''.join(pattern)

def entropy(guess, possible):
    counts = {}
    for w in possible:
        p = feedback(guess, w)
        counts[p] = counts.get(p, 0) + 1

    total = len(possible)
    e = 0
    for c in counts.values():
        p = c / total
        e -= p * math.log2(p)
    return e

def score(word, possible):
    freq = {}
    for w in possible:
        for c in set(w):
            freq[c] = freq.get(c, 0) + 1
    return sum(freq.get(c, 0) for c in set(word))

# -----------------------------
# STATE (ENTROPY)
# -----------------------------
if "entropy_guesses" not in st.session_state:
    st.session_state.entropy_guesses, st.session_state.entropy_solutions = load_lists()

if "entropy_possible" not in st.session_state:
    st.session_state.entropy_possible = st.session_state.entropy_solutions.copy()

if "entropy_history" not in st.session_state:
    st.session_state.entropy_history = []

if "entropy_round" not in st.session_state:
    st.session_state.entropy_round = 1

# Reset
if st.sidebar.button("🔁 Reset"):
    st.session_state.entropy_possible = st.session_state.entropy_solutions.copy()
    st.session_state.entropy_history = []
    st.session_state.entropy_round = 1
    st.rerun()

# -----------------------------
# INPUT
# -----------------------------
if not st.session_state.entropy_history:
    st.info("🎯 Start with your first guess")

guess = st.text_input("Guess").upper().strip()
fb = st.text_input("Feedback (G/Y/B)").upper().strip()

# -----------------------------
# ANALYZE
# -----------------------------
if st.button("Analyze"):

    if len(guess) != 5 or len(fb) != 5:
        st.warning("Enter valid input.")

    elif st.session_state.entropy_round > 6:
        st.error("❌ Max 6 guesses reached. Reset.")

    else:
        st.session_state.entropy_history.append((guess, fb))

        if fb != "GGGGG":
            st.session_state.entropy_possible = [
                w for w in st.session_state.entropy_possible
                if feedback(guess, w) == fb
            ]

        st.session_state.entropy_round += 1

# -----------------------------
# RESULTS
# -----------------------------
if st.session_state.entropy_history:
    last_guess, last_fb = st.session_state.entropy_history[-1]

    st.markdown("---")

    if last_fb == "GGGGG":
        st.success(f"🎉 Solved in {st.session_state.entropy_round - 1} guesses!")
    else:
        st.subheader(f"Round {st.session_state.entropy_round - 1}")
        st.write(f"Remaining candidates: {len(st.session_state.entropy_possible)}")

        if len(st.session_state.entropy_possible) > 5:
            subset = st.session_state.entropy_guesses[:800]
            best = max(subset, key=lambda g: entropy(g, st.session_state.entropy_possible))
            st.write(f"Best guess (entropy): {best}")
        else:
            best = max(st.session_state.entropy_possible, key=lambda w: score(w, st.session_state.entropy_possible))
            st.write(f"Best guess (solution-based): {best}")

# -----------------------------
# HISTORY
# -----------------------------
st.markdown("---")
st.subheader("History")

if st.session_state.entropy_history:
    df = pd.DataFrame(st.session_state.entropy_history, columns=["Guess", "Feedback"])
    st.table(df)
else:
    st.info("No guesses yet.")