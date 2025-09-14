from langmachines.dfa import DFA
from langmachines.algorithms.minimize import minimize_dfa


def test_hopcroft_minimizes_even_zeros():
    q0, q1 = "q0", "q1"
    d = DFA(
        states={q0, q1},
        alphabet={"0", "1"},
        start=q0,
        accept={q0},
        delta={
            (q0, "0"): q1, (q0, "1"): q0,
            (q1, "0"): q0, (q1, "1"): q1,
        },
    )
    m = minimize_dfa(d)
    assert len(m.states) == 2
    assert m.start in m.states
    # Accepting set should be exactly one of the two minimized states
    assert len(m.accept) == 1


def test_minimize_with_unreachable_and_sink():
    d2 = DFA(
        states={"A", "B", "C_unreach"},
        alphabet={"a", "b"},
        start="A",
        accept={"B"},
        delta={
            ("A", "a"): "B",  # ("A","b") missing -> potential sink
            ("B", "a"): "B", ("B", "b"): "A",
        },
    )
    m2 = minimize_dfa(d2)
    # Either 2 or 3 states depending on whether sink is reachable
    assert 2 <= len(m2.states) <= 3
    # Start maps somewhere valid
    assert m2.start in m2.states
