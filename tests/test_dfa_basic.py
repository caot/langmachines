from langmachines.dfa import DFA, simulate, prune_unreachable, totalize


def test_simulate_even_zeros():
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
    assert simulate(d, "1") is True
    assert simulate(d, "0") is False
    assert simulate(d, "10") is False
    assert simulate(d, "1010") is True


def test_prune_and_totalize():
    d = DFA(
        states={"A", "B", "C_unreach"},
        alphabet={"a", "b"},
        start="A",
        accept={"B"},
        delta={
            ("A", "a"): "B",
            ("B", "a"): "B", ("B", "b"): "A",
            # C_unreach has no incoming transitions
        },
    )
    p = prune_unreachable(d)
    assert "C_unreach" not in p.states

    t = totalize(p)
    for s in t.states:
        for a in t.alphabet:
            assert (s, a) in t.delta
