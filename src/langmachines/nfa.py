from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, Tuple

from .dfa import DFA, State, Symbol

EPSILON = "ε"  # reserved symbol for epsilon transitions


@dataclass(frozen=True)
class NFA:
    states: Set[State]
    alphabet: Set[Symbol]
    start: State
    accept: Set[State]
    delta: Dict[Tuple[State, Symbol], Set[State]]


def epsilon_closure(nfa: NFA, states: Set[State]) -> Set[State]:
    """
    Compute the ε-closure of a set of states in the NFA.
    That is, all states reachable by following ε-transitions (including the input states).
    """
    closure = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for t in nfa.delta.get((s, EPSILON), set()):
            if t not in closure:
                closure.add(t)
                stack.append(t)
    return closure


def move(nfa: NFA, states: Set[State], symbol: Symbol) -> Set[State]:
    """
    From a set of states, follow `symbol` transitions (excluding ε).
    """
    nxt = set()
    for s in states:
        nxt |= nfa.delta.get((s, symbol), set())
    return nxt


def to_dfa(nfa: NFA) -> DFA:
    """
    Subset construction (a.k.a. powerset construction).
    Converts an NFA (with ε-transitions) into an equivalent DFA.
    """

    # Start state is ε-closure of NFA start
    start_closure = frozenset(epsilon_closure(nfa, {nfa.start}))

    unmarked: list[frozenset[State]] = [start_closure]
    dfa_states: Set[frozenset[State]] = {start_closure}
    dfa_delta: Dict[Tuple[frozenset[State], Symbol], frozenset[State]] = {}
    dfa_accept: Set[frozenset[State]] = set()

    while unmarked:
        S = unmarked.pop()
        if any(s in nfa.accept for s in S):
            dfa_accept.add(S)

        for a in nfa.alphabet:
            # ignore ε in DFA alphabet
            if a == EPSILON:
                continue
            # compute move + ε-closure
            T = epsilon_closure(nfa, move(nfa, S, a))
            if not T:
                continue
            T_frozen = frozenset(T)
            dfa_delta[(S, a)] = T_frozen
            if T_frozen not in dfa_states:
                dfa_states.add(T_frozen)
                unmarked.append(T_frozen)

    # Convert frozensets to string names (stable identifiers)
    state_names: Dict[frozenset[State], str] = {}
    for i, S in enumerate(sorted(dfa_states, key=lambda s: sorted(map(str, s)))):
        state_names[S] = f"Q{i}"

    new_states = set(state_names.values())
    new_start = state_names[start_closure]
    new_accept = {state_names[S] for S in dfa_accept}
    new_delta = {}
    for (S, a), T in dfa_delta.items():
        new_delta[(state_names[S], a)] = state_names[T]

    return DFA(
        states=new_states,
        alphabet={a for a in nfa.alphabet if a != EPSILON},
        start=new_start,
        accept=new_accept,
        delta=new_delta,
    )
