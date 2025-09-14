from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Dict, Set, Tuple, Hashable, Iterable

State = Hashable
Symbol = Hashable


@dataclass(frozen=True)
class DFA:
    states: Set[State]
    alphabet: Set[Symbol]
    start: State
    accept: Set[State]
    delta: Dict[Tuple[State, Symbol], State]


def simulate(dfa: DFA, input_symbols: Iterable[Symbol]) -> bool:
    """
    Run the DFA on an iterable of symbols.
    Returns True iff the final state is accepting.
    """
    if dfa.start not in dfa.states:
        raise ValueError("Start state is not in DFA states.")
    q = dfa.start
    for a in input_symbols:
        if a not in dfa.alphabet:
            raise KeyError(f"Symbol {a!r} not in alphabet.")
        q = dfa.delta.get((q, a))
        if q is None:
            # Partial DFA: missing transition means reject
            return False
    return q in dfa.accept


def prune_unreachable(dfa: DFA) -> DFA:
    """
    Keep only states reachable from the start via zero or more transitions.
    Drops transitions leaving the reachable subgraph.
    """
    from collections import deque

    seen: Set[State] = set()
    Q = deque([dfa.start])
    while Q:
        s = Q.popleft()
        if s in seen:
            continue
        seen.add(s)
        for a in dfa.alphabet:
            t = dfa.delta.get((s, a))
            if t is not None and t not in seen:
                Q.append(t)

    new_delta = {k: v for k, v in dfa.delta.items() if k[0] in seen and v in seen}
    new_accept = dfa.accept & seen
    return replace(dfa, states=seen, accept=new_accept, delta=new_delta)


def totalize(dfa: DFA) -> DFA:
    """
    Ensure the DFA is total by adding a fresh sink state if needed.
    If no missing transitions exist, returns the DFA unchanged.
    """
    sink_needed = False
    for s in dfa.states:
        for a in dfa.alphabet:
            if (s, a) not in dfa.delta:
                sink_needed = True
                break
        if sink_needed:
            break

    if not sink_needed:
        return dfa

    sink = object()  # unique sentinel
    states = set(dfa.states) | {sink}
    delta = dict(dfa.delta)
    for s in states:
        for a in dfa.alphabet:
            if (s, a) not in delta:
                delta[(s, a)] = sink
    accept = set(dfa.accept)  # sink is non-accepting
    return DFA(states=states, alphabet=set(dfa.alphabet), start=dfa.start, accept=accept, delta=delta)
