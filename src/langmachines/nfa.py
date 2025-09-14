from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, Tuple, Hashable, FrozenSet, AbstractSet

from .dfa import DFA, State, Symbol

EPSILON = "ε"  # reserved symbol for epsilon transitions


@dataclass(frozen=True)
class NFA:
    states: Set[State]
    alphabet: Set[Symbol]
    start: State
    accept: Set[State]
    delta: Dict[Tuple[State, Symbol], Set[State]]


def epsilon_closure(nfa: NFA, states: AbstractSet[State]) -> Set[State]:
    """
    Compute the ε-closure of a set of states in the NFA.
    Accepts any set-like (set/frozenset).
    """
    closure: Set[State] = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for t in nfa.delta.get((s, EPSILON), set()):
            if t not in closure:
                closure.add(t)
                stack.append(t)
    return closure


def move(nfa: NFA, states: AbstractSet[State], symbol: Symbol) -> Set[State]:
    """
    From a set of states, follow `symbol` transitions (excluding ε).
    Accepts any set-like (set/frozenset).
    """
    nxt: Set[State] = set()
    for s in states:
        nxt |= nfa.delta.get((s, symbol), set())
    return nxt


def to_dfa(nfa: NFA) -> DFA:
    """
    Subset (powerset) construction from NFA (with ε) to equivalent DFA.
    Internally represents DFA states as FrozenSet[State].
    """
    # Start is ε-closure of NFA start
    start_closure: FrozenSet[State] = frozenset(epsilon_closure(nfa, {nfa.start}))

    unmarked: list[FrozenSet[State]] = [start_closure]
    dfa_states: Set[FrozenSet[State]] = {start_closure}
    dfa_delta: Dict[Tuple[FrozenSet[State], Symbol], FrozenSet[State]] = {}
    dfa_accept: Set[FrozenSet[State]] = set()

    while unmarked:
        S = unmarked.pop()
        if any(s in nfa.accept for s in S):
            dfa_accept.add(S)

        for a in nfa.alphabet:
            if a == EPSILON:
                continue
            # compute move + ε-closure; freeze to be a valid DFA state key
            T_set = epsilon_closure(nfa, move(nfa, S, a))
            if not T_set:
                continue
            T: FrozenSet[State] = frozenset(T_set)
            dfa_delta[(S, a)] = T
            if T not in dfa_states:
                dfa_states.add(T)
                unmarked.append(T)

    # Give stable string names to each DFA state
    state_names: Dict[FrozenSet[State], str] = {}
    for i, S in enumerate(sorted(dfa_states, key=lambda ss: tuple(sorted(map(str, ss))))):
        state_names[S] = f"Q{i}"

    # Assemble DFA with Hashable-typed containers to satisfy DFA signature
    new_states: Set[Hashable] = set(state_names.values())
    new_start: Hashable = state_names[start_closure]
    new_accept: Set[Hashable] = {state_names[S] for S in dfa_accept}
    new_delta: Dict[Tuple[Hashable, Hashable], Hashable] = {}
    for (S, a), T in dfa_delta.items():
        new_delta[(state_names[S], a)] = state_names[T]

    return DFA(
        states=new_states,
        alphabet={a for a in nfa.alphabet if a != EPSILON},
        start=new_start,
        accept=new_accept,
        delta=new_delta,
    )
