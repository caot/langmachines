from __future__ import annotations

from typing import Tuple, Hashable, Dict, Set
from ..dfa import DFA, State

def dfa_to_dot(dfa: DFA, *, rankdir: str = "LR", name: str = "DFA") -> str:
    """
    Return a Graphviz DOT string for a DFA.
    - No external deps required.
    - Edges with the same (src, dst) are merged with comma-joined labels.
    """
    # Group labels for same (src, dst)
    edge_labels: Dict[Tuple[State, State], Set[str]] = {}
    for (s, a), t in dfa.delta.items():
        edge_labels.setdefault((s, t), set()).add(str(a))

    def q(s: Hashable) -> str:
        # DOT-safe id (quote strings; leave simple identifiers alone)
        sid = str(s)
        if sid.isidentifier():
            return sid
        return f"\"{sid}\""

    lines = []
    lines.append(f'digraph {name} {{')
    lines.append(f'  rankdir={rankdir};')
    lines.append('  node [shape=circle];')

    # Invisible start arrow
    lines.append('  __start__ [shape=point, style=invis, width=0];')
    lines.append(f'  __start__ -> {q(dfa.start)} [label="start"];')

    # Accepting states as doublecircle
    if dfa.accept:
        acc_nodes = " ".join(q(s) for s in dfa.accept)
        lines.append('  subgraph cluster_accept {{ label="accepting"; color=gray80; style=dashed;')
        lines.append('    node [shape=doublecircle];')
        lines.append(f'    {acc_nodes};')
        lines.append('  }')

    # Non-accepting nodes (ensure they exist even if no edges)
    nonacc = dfa.states - dfa.accept
    if nonacc:
        nodes = " ".join(q(s) for s in nonacc)
        lines.append(f'  {nodes};')

    # Edges with merged labels
    for (s, t), labels in sorted(edge_labels.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        label = ", ".join(sorted(labels, key=str))
        lines.append(f'  {q(s)} -> {q(t)} [label="{label}"];')

    lines.append('}')
    return "\n".join(lines)


def render_dfa(
    dfa: DFA,
    *,
    format: str = "png",
    filename: str | None = None,
    rankdir: str = "LR",
    name: str = "DFA",
):
    """
    Render the DFA to an image using the optional 'graphviz' package.
    Returns the path to the rendered file (without extension if filename not given).

    Usage:
        pip install ".[viz]"
        render_dfa(dfa, format="svg", filename="out/dfa_even_zeros")

    If 'graphviz' is not installed, raises ImportError.
    """
    try:
        from graphviz import Source
    except Exception as e:  # pragma: no cover
        raise ImportError(
            "render_dfa requires the 'graphviz' Python package. "
            "Install extras: pip install '.[viz]'"
        ) from e

    dot = dfa_to_dot(dfa, rankdir=rankdir, name=name)
    src = Source(dot, filename=filename, format=format)
    outpath = src.render(cleanup=True)  # returns path incl. extension
    return outpath
