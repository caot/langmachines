from langmachines.nfa import NFA, EPSILON, epsilon_closure, to_dfa
from langmachines.dfa import simulate


def test_epsilon_closure_basic():
    # Graph:
    # A -ε-> B -ε-> C
    # D isolated
    nfa = NFA(
        states={"A", "B", "C", "D"},
        alphabet={EPSILON},
        start="A",
        accept={"C"},
        delta={
            ("A", EPSILON): {"B"},
            ("B", EPSILON): {"C"},
        },
    )
    assert epsilon_closure(nfa, {"A"}) == {"A", "B", "C"}
    assert epsilon_closure(nfa, {"B"}) == {"B", "C"}
    assert epsilon_closure(nfa, {"C"}) == {"C"}
    assert epsilon_closure(nfa, {"D"}) == {"D"}


def test_subset_construction_union_via_epsilon():
    # Language: 'a' ∪ 'ab'
    # NFA:
    #   s -ε-> s1 -a-> f
    #   s -ε-> s2 -a-> t -b-> f
    s, s1, s2, t, f = "s", "s1", "s2", "t", "f"
    nfa = NFA(
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

    dfa = to_dfa(nfa)
    # Basic sanity: DFA alphabet excludes EPSILON
    assert EPSILON not in dfa.alphabet
    assert dfa.alphabet == {"a", "b"}

    # The resulting DFA should accept exactly {'a', 'ab'}
    assert simulate(dfa, "") is False
    assert simulate(dfa, "a") is True
    assert simulate(dfa, "ab") is True
    assert simulate(dfa, "b") is False
    assert simulate(dfa, "aa") is False
    assert simulate(dfa, "aba") is False


def test_nfa_with_epsilon_accepts_empty_string():
    # NFA where start -ε-> accept, so empty string is accepted.
    nfa = NFA(
        states={"A", "B"},
        alphabet={"0", EPSILON},
        start="A",
        accept={"B"},
        delta={
            ("A", EPSILON): {"B"},
            ("A", "0"): {"A"},
        },
    )
    dfa = to_dfa(nfa)
    assert simulate(dfa, "") is True
    assert simulate(dfa, "0") is True
    assert simulate(dfa, "000") is True
