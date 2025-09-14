from langmachines.dfa import DFA
from langmachines.algorithms.minimize import minimize_dfa
from langmachines import dfa_to_dot, render_dfa

q0, q1 = "q0", "q1"
dfa = DFA(
    states={q0, q1},
    alphabet={"0", "1"},
    start=q0,
    accept={q0},
    delta={
        (q0, "0"): q1, (q0, "1"): q0,
        (q1, "0"): q0, (q1, "1"): q1,
    },
)

m = minimize_dfa(dfa)

# 1) Just print DOT (no deps)
print(dfa_to_dot(m, name="EvenZerosMin"))

# 2) Optionally render to SVG/PNG (needs extras + system graphviz)
try:
    path = render_dfa(m, format="svg", filename="out/even_zeros_min")
    print("Rendered to:", path)
except ImportError as e:
    print(e)
