# examples/nfa_union_ab.py
# Demonstrates an NFA for the language {'a', 'ab'} using ε-transitions,
# converts it to a DFA via subset construction, and runs a few acceptance checks.

from langmachines.nfa import NFA, EPSILON, to_dfa
from langmachines.dfa import simulate
from langmachines import dfa_to_dot

def build_nfa_union_ab() -> NFA:
    # NFA structure:
    #   s -ε-> s1 -a-> f
    #   s -ε-> s2 -a-> t -b-> f
    s, s1, s2, t, f = "s", "s1", "s2", "t", "f"
    return NFA(
        states={s, s1, s2, t, f},
        alphabet={"a", "b", EPSILON},
        start=s,
        accept={f},
        delta={
            (s, EPSILON): {s1, s2},
            (s1, "a"): {f},
            (s2, "a"): {t},
            (t, "b"): {f},
        },
    )

def main() -> None:
    nfa = build_nfa_union_ab()
    dfa = to_dfa(nfa)

    print("DFA states:", dfa.states)
    print("Start:", dfa.start)
    print("Accept:", dfa.accept)
    print("Delta:")
    for (q, a), r in sorted(dfa.delta.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        print(f"  δ({q!r}, {a!r}) = {r!r}")

    # Try a few strings
    tests = ["", "a", "b", "ab", "aa", "aba"]
    print("\nAcceptance:")
    for s in tests:
        print(f"  {s!r}: {'ACCEPT' if simulate(dfa, s) else 'REJECT'}")

    # Print DOT (text) for quick visualization
    print("\nDOT representation (minimized not applied here):")
    print(dfa_to_dot(dfa, name="NFA_Union_ab_DFA"))

if __name__ == "__main__":
    main()
