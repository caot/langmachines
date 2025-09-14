from langmachines.dfa import DFA
from langmachines import dfa_to_dot

def test_dfa_to_dot_contains_states_and_edges():
    d = DFA(
        states={"A", "B"},
        alphabet={"x"},
        start="A",
        accept={"B"},
        delta={("A", "x"): "B", ("B", "x"): "B"},
    )
    dot = dfa_to_dot(d, name="TestDFA")
    assert "digraph TestDFA" in dot
    assert "A -> B" in dot
    assert "shape=doublecircle" in dot  # accepting style
