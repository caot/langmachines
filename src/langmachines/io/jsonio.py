from __future__ import annotations
from typing import Dict, Any, Hashable, Tuple, Set
import json

from ..dfa import DFA


def dfa_from_json_obj(obj: Dict[str, Any]) -> DFA:
    if obj.get("type") != "dfa":
        raise ValueError("JSON does not describe a DFA (missing type='dfa').")
    # Annotate as Hashable so mypy is happy even though most JSON uses str.
    states: Set[Hashable] = set(obj["states"])
    alphabet: Set[Hashable] = set(obj["alphabet"])
    start: Hashable = obj["start"]
    accept: Set[Hashable] = set(obj["accept"])
    delta_nested: Dict[str, Dict[str, str]] = obj["delta"]

    # Important: annotate delta with Hashable types to satisfy DFA signature.
    delta: Dict[Tuple[Hashable, Hashable], Hashable] = {}
    for s, row in delta_nested.items():
        for a, t in row.items():
            delta[(s, a)] = t

    return DFA(states=states, alphabet=alphabet, start=start, accept=accept, delta=delta)


def dfa_to_json_obj(dfa: DFA) -> Dict[str, Any]:
    nested: Dict[str, Dict[str, str]] = {}
    for (s, a), t in dfa.delta.items():
        nested.setdefault(str(s), {})[str(a)] = str(t)
    return {
        "type": "dfa",
        "states": [str(s) for s in dfa.states],
        "alphabet": [str(a) for a in dfa.alphabet],
        "start": str(dfa.start),
        "accept": [str(s) for s in dfa.accept],
        "delta": nested,
    }


def load_dfa(path: str) -> DFA:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    return dfa_from_json_obj(obj)


def save_dfa(dfa: DFA, path: str) -> None:
    obj = dfa_to_json_obj(dfa)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
