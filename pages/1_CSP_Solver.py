import streamlit as st
import pandas as pd

st.set_page_config(page_title="Wordle Solver (CSP)", page_icon="🧠")

st.title("🧠 Wordle Solver (CSP)")

# -----------------------------
# LOAD
# -----------------------------
@st.cache_data
def load_solutions():
    df = pd.read_csv("valid_solutions.csv")
    return [w.upper() for w in df["word"] if len(w) == 5]

# -----------------------------
# WORDLE LOGIC
# -----------------------------
def feedback(guess, target):
    result = [""] * 5
    target_chars = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "G"
            target_chars[i] = None

    for i in range(5):
        if result[i] == "":
            if guess[i] in target_chars:
                result[i] = "Y"
                target_chars[target_chars.index(guess[i])] = None
            else:
                result[i] = "B"

    return "".join(result)

def match(word, guess, fb):
    return feedback(guess, word) == fb

def score(word, possible):
    freq = {}
    for w in possible:
        for c in set(w):
            freq[c] = freq.get(c, 0) + 1
    return sum(freq.get(c, 0) for c in set(word))

# -----------------------------
# STATE
# -----------------------------
if "csp_possible" not in st.session_state:
    st.session_state.csp_possible = load_solutions()

if "csp_history" not in st.session_state:
    st.session_state.csp_history = []

if "csp_round" not in st.session_state:
    st.session_state.csp_round = 1

# Reset
if st.sidebar.button("🔁 Reset"):
    st.session_state.csp_possible = load_solutions()
    st.session_state.csp_history = []
    st.session_state.csp_round = 1
    st.rerun()

# -----------------------------
# UI
# -----------------------------
st.info("🎯 Start with your first guess")

guess = st.text_input("Guess").upper().strip()
fb = st.text_input("Feedback (G/Y/B)").upper().strip()

# -----------------------------
# ANALYZE
# -----------------------------
if st.button("Analyze"):

    if len(guess) == 5 and len(fb) == 5:

        st.session_state.csp_history.append((guess, fb))

        if fb != "GGGGG":
            st.session_state.csp_possible = [
                w for w in st.session_state.csp_possible
                if match(w, guess, fb)
            ]

        st.session_state.csp_round += 1

# -----------------------------
# RESULTS
# -----------------------------
if st.session_state.csp_history:

    last_guess, last_fb = st.session_state.csp_history[-1]

    st.markdown("---")

    if last_fb == "GGGGG":
        st.success(f"🎉 Solved in {st.session_state.csp_round - 1} guesses!")
    else:
        st.write(f"Remaining candidates: {len(st.session_state.csp_possible)}")

        ranked = sorted(
            [(w, score(w, st.session_state.csp_possible)) for w in st.session_state.csp_possible],
            key=lambda x: x[1],
            reverse=True
        )[:10]

        st.write("Top suggestions:")
        for w, s in ranked:
            st.write(f"{w} ({s})")

# -----------------------------
# HISTORY (MATCHED STYLE)
# -----------------------------
st.markdown("---")
st.subheader("History")

if st.session_state.csp_history:
    df = pd.DataFrame(st.session_state.csp_history, columns=["Guess", "Feedback"])
    st.table(df)
else:
    st.info("No guesses yet.")