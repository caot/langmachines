# langmachines

*A lightweight, extensible toolkit for automata, formal languages, and algorithms — designed for research, teaching, and AI applications.*

---

## ✨ Overview

`langmachines` provides core data structures and algorithms for working with **language machines** — finite automata, regular expressions, and beyond. It’s built to be:

- **Lightweight** → zero dependencies by default  
- **Research-friendly** → readable implementations of classic algorithms  
- **Extensible** → clean API to experiment with your own automata, grammars, or learning methods  
- **Visualizable** → optional Graphviz export for state diagrams  
- **AI-aligned** → a sandbox for exploring automata-theoretic approaches to learning, reasoning, and formal verification  

---

## 🚀 Features (current & planned)

- **Deterministic Finite Automata (DFA)**
  - Simulation & recognition
  - Pruning unreachable states
  - Totalization with sink states
  - **Hopcroft’s algorithm** for DFA minimization  

- **Nondeterministic Finite Automata (NFA)** *(planned)*
  - ε-closure & subset construction  
  - Conversion to DFA  

- **Regular Expressions → Automata** *(planned)*
  - Thompson’s construction  
  - Simplification  

- **Algorithms Library** *(expanding)*
  - Product construction (union, intersection)  
  - Complement & difference  
  - Equivalence checking  

- **I/O & Visualization**
  - JSON import/export  
  - DOT export for Graphviz (`dfa_to_dot`)  
  - Optional rendering with `graphviz` Python package (`render_dfa`)  

- **Research & AI Directions**
  - Automata learning (e.g., Angluin’s L* algorithm)  
  - Symbolic automata and decision procedures  
  - Formal verification experiments  
  - Bridging classical automata with modern AI models  

---

## 📦 Installation

### Core (no dependencies)
```bash
pip install langmachines
```

### With visualization support
```bash
pip install "langmachines[viz]"
```
> Requires [Graphviz system binaries](https://graphviz.org/download/).

---

## 🧑‍💻 Quickstart

```python
from langmachines.dfa import DFA
from langmachines.algorithms.minimize import minimize_dfa

# DFA for even number of '0's
q0, q1 = "q0", "q1"
dfa = DFA(
    states={q0, q1},
    alphabet={"0", "1"},
    start=q0,
    accept={q0},
    delta={
        (q0,"0"): q1, (q0,"1"): q0,
        (q1,"0"): q0, (q1,"1"): q1,
    }
)

m = minimize_dfa(dfa)
print("States:", m.states)
print("Accept:", m.accept)
print("Block map:", m.block_of)
```

### DOT export
```python
from langmachines import dfa_to_dot

print(dfa_to_dot(m))
```

### Render as SVG
```python
from langmachines import render_dfa
render_dfa(m, format="svg", filename="out/even_zeros_min")
```

---

## 📂 Project structure

```
src/langmachines/
├─ dfa.py           # DFA types & utilities
├─ nfa.py           # NFA support (planned)
├─ regex.py         # Regex → automata (planned)
├─ algorithms/      # Minimization, equivalence, etc.
├─ io/              # DOT & JSON I/O
└─ utils.py
```

---

## 🛠 Development Setup

We use a **src-layout** (`src/langmachines/…`) so imports stay clean when installed, but this means you should install the package locally before running examples or tests.

### 1. Clone and enter the repo
```bash
git clone https://github.com/caot/langmachines.git
cd langmachines
```

### 2. Install in editable mode
```bash
pip install -e ".[dev]"
```

- `-e` → editable install (changes in `src/` are picked up instantly).  
- `.[dev]` → also installs test/lint deps (`pytest`, `mypy`, `ruff`).  

### 3. Run examples
```bash
python examples/minimize_even_zeros.py
```

Or, without installing (not recommended):
```bash
PYTHONPATH=src python examples/minimize_even_zeros.py
```

### 4. Run tests
```bash
pytest -q
```

### 5. Optional: visualization support
```bash
pip install ".[viz]"
# and ensure Graphviz system binaries (dot) are installed
```

---

## 🌍 Roadmap

- [x] DFA + Hopcroft minimization  
- [ ] NFA & ε-closure utilities  
- [ ] Regex → NFA → DFA conversion  
- [ ] Automata operations (union, intersection, difference)  
- [ ] Equivalence & inclusion checking  
- [ ] CLI (`langmachines minimize <dfa.json>`)  
- [ ] Research extensions:
  - Active automata learning (L*, Rivest–Schapire)  
  - Symbolic automata for large alphabets  
  - Links to AI/ML pipelines (grammar induction, RNN/automata comparisons)  

---

## 📚 Who is this for?

- **Researchers** in AI, algorithms, or formal languages  
- **Students** studying automata theory or compiler design  
- **Educators** teaching computation theory with practical demos  
- **Builders** exploring how automata concepts connect to modern ML  

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📖 License

MIT — free to use, modify, and share. Contributions welcome!  

---

💡 *The name* `langmachines` *is inspired by the idea that automata are “machines of language,” bridging formal languages and intelligent computation.*
