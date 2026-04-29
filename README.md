# 🧠 Wordle Solver — CSP vs Entropy Optimization

A high-performance Wordle solver that compares constraint-based reasoning with information-theoretic optimization.

---

## 🚀 Live Demo

👉 https://wordle--solver.streamlit.app/

---

## 📌 Overview

This project implements two independent approaches to solving Wordle:

- 🔐 CSP Solver — eliminates invalid solutions using strict constraints  
- 🤖 Hybrid Entropy Solver — selects guesses that maximize information gain  

Both models operate on official Wordle datasets and simulate real gameplay.

---

## 🧠 Approach

### 🔐 CSP (Constraint Satisfaction Problem)

- Applies Wordle feedback rules (G/Y/B)  
- Filters candidate solutions  
- Uses letter-frequency scoring for suggestions  

**Strengths:**
- Deterministic and fast  
- Strong convergence in later stages  

---

### 🤖 Hybrid Entropy Solver

- Uses entropy to maximize information gain  
- Evaluates how guesses split the solution space  
- Switches to solution-based scoring when candidates are small  

**Strengths:**
- Better exploration early in the game  
- Higher success rate overall  

---

## 📊 Performance

Evaluated across all 2315 official Wordle solutions:

| Model           | Avg Guesses | Max Guesses | Success Rate |
|----------------|------------|------------|-------------|
| CSP Solver     | 3.65       | 6          | 99.05%      |
| Hybrid Solver  | 3.68       | 6          | 99.78%      |

---

## 🗂️ Project Structure
wordle-solver/
│
├── app.py
├── evaluation.py
├── valid_guesses.csv
├── valid_solutions.csv
├── requirements.txt
│
└── pages/
├── 1_CSP_Solver.py
└── 2_Entropy_Solver.py

---

## ⚙️ Run Locally
- pip install -r requirements.txt
- streamlit run app.py

---

## 🧪 Evaluation

The evaluation system:
- Simulates all Wordle solutions  
- Measures average guesses, success rate, and worst-case performance  

---

## 🎯 Key Insights

- Entropy improves exploration in early guesses  
- CSP improves convergence in constrained states  
- Hybrid approach balances exploration and exploitation  

---

## 🔮 Future Work

- Parallelize entropy computation  
- Optimize guess space pruning  
- Add visualization of information gain  
- Extend to different word lengths  

---

## 👤 Author

Vidit Choudhary

---

## ⭐

If you found this useful, consider giving it a star ⭐
