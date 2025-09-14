from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Dict, Set, Tuple, FrozenSet

from ..dfa import DFA, State, Symbol, prune_unreachable


@dataclass(frozen=True)
class MinDFA(DFA):
    # Map each original (reachable) state to the representative of its minimized block
    block_of: Dict[State, State]


def minimize_dfa(dfa: DFA) -> MinDFA:
    """
    Hopcroft DFA minimization.
    - Prunes unreachable states
    - Totalizes only if necessary by adding a sink (and only keeps it if reachable)
    - Returns a language-equivalent minimal DFA as MinDFA
    """
    if dfa.start not in dfa.states:
        raise ValueError("Start state not in states.")
    if not dfa.accept.issubset(dfa.states):
        raise ValueError("Accepting states must be subset of states.")

    # 1) Restrict to reachable states
    dfa = prune_unreachable(dfa)
    if not dfa.states:
        # Degenerate: no reachable states (shouldn’t normally happen if start exists)
        return MinDFA(states=set(), alphabet=set(dfa.alphabet), start=None, accept=set(), delta={}, block_of={})

    # 2) Totalize only if needed and check if sink becomes reachable
    needs_sink = any((s, a) not in dfa.delta for s in dfa.states for a in dfa.alphabet)
    sink = None
    delta: Dict[Tuple[State, Symbol], State] = {}

    if needs_sink:
        sink = object()
        # Provisional transitions
        for s in dfa.states | {sink}:
            for a in dfa.alphabet:
                if s is sink:
                    delta[(sink, a)] = sink
                else:
                    delta[(s, a)] = dfa.delta.get((s, a), sink)
        # Check if sink is actually reached from the start
        sink_reached = _reachable_to_sink(dfa.start, dfa.states | {sink}, dfa.alphabet, delta, sink)
        if sink_reached:
            states = set(dfa.states) | {sink}
        else:
            # drop sink transitions
            delta = {(s, a): t for (s, a), t in delta.items() if s is not sink}
            states = set(dfa.states)
            sink = None
    else:
        delta = dict(dfa.delta)
        states = set(dfa.states)

    accept = set(dfa.accept)

    # 3) Hopcroft
    nonaccept = states - accept
    P: Set[FrozenSet[State]] = set()
    if accept:
        P.add(frozenset(accept))
    if nonaccept:
        P.add(frozenset(nonaccept))

    W: Set[Tuple[FrozenSet[State], Symbol]] = set()
    if accept and nonaccept:
        smaller = accept if len(accept) <= len(nonaccept) else nonaccept
        for a in dfa.alphabet:
            W.add((frozenset(smaller), a))

    inv: Dict[Tuple[Symbol, State], Set[State]] = defaultdict(set)
    for (s, a), t in delta.items():
        inv[(a, t)].add(s)

    while W:
        A, a = W.pop()
        pred = set()
        for q in A:
            pred |= inv.get((a, q), set())

        newP: Set[FrozenSet[State]] = set()
        for Y in P:
            Y1 = Y & pred
            if not Y1:
                newP.add(Y)
                continue
            Y2 = Y - pred
            if not Y2:
                newP.add(Y)
                continue

            newP.add(frozenset(Y1))
            newP.add(frozenset(Y2))

            if (Y, a) in W:
                W.remove((Y, a))
                W.add((frozenset(Y1), a))
                W.add((frozenset(Y2), a))
            else:
                add_block = frozenset(Y1) if len(Y1) <= len(Y2) else frozenset(Y2)
                for c in dfa.alphabet:
                    W.add((add_block, c))
        P = newP

    # 4) Build quotient
    def rep(block: FrozenSet[State]) -> State:
        return sorted(block, key=lambda x: str(x))[0]

    block_by_state: Dict[State, FrozenSet[State]] = {}
    for B in P:
        for s in B:
            block_by_state[s] = B

    new_states: Set[State] = set()
    new_accept: Set[State] = set()
    new_delta: Dict[Tuple[State, Symbol], State] = {}

    for B in P:
        r = rep(B)
        new_states.add(r)
        if any(s in accept for s in B):
            new_accept.add(r)

    new_start = rep(block_by_state[dfa.start])

    for B in P:
        r = rep(B)
        # Any representative works for transitions
        sample = next(iter(B))
        for a in dfa.alphabet:
            t = delta[(sample, a)]
            new_delta[(r, a)] = rep(block_by_state[t])

    # Map original (reachable) states to representatives; skip synthetic sink
    original_states = states - ({sink} if sink is not None else set())
    block_of = {s: rep(block_by_state[s]) for s in original_states}

    return MinDFA(
        states=new_states,
        alphabet=set(dfa.alphabet),
        start=new_start,
        accept=new_accept,
        delta=new_delta,
        block_of=block_of,
    )


def _reachable_to_sink(start: State, states: Set[State], alphabet: Set[Symbol],
                       delta: Dict[Tuple[State, Symbol], State], sink: State) -> bool:
    """BFS to check whether the synthetic sink is reachable from start."""
    Q = deque([start])
    seen = set()
    while Q:
        s = Q.popleft()
        if s in seen:
            continue
        seen.add(s)
        for a in alphabet:
            t = delta[(s, a)]
            if t is sink:
                return True
            if t in states and t not in seen:
                Q.append(t)
    return False
