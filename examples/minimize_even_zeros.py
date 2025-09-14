from langmachines.dfa import DFA
from langmachines.algorithms.minimize import minimize_dfa

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
print("States:", m.states)
print("Start:", m.start)
print("Accept:", m.accept)
print("Delta:")
for (s, a), t in sorted(m.delta.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
    print(f"  δ({s!r}, {a!r}) = {t!r}")

print("Block mapping (old -> new):", m.block_of)
