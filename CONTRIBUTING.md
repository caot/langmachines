# Contributing to `langmachines`

Thanks for considering contributing! 🎉  
This project is meant as a clean, research-friendly toolkit for **automata, algorithms, and AI experiments**. Contributions of all kinds are welcome: bug fixes, new algorithms, documentation, or examples.

---

## 🛠 Development Setup

1. **Fork & clone**
   ```bash
   git clone https://github.com/caot/langmachines.git
   cd langmachines
   ```

2. **Install in editable mode**
   ```bash
   pip install -e ".[dev]"
   ```
   - `-e` → editable install (changes in `src/` are picked up instantly).
   - `.[dev]` → installs testing & linting tools.

3. **Optional visualization support**
   ```bash
   pip install ".[viz]"
   ```
   Requires [Graphviz binaries](https://graphviz.org/download/).

---

## ✅ PR Checklist

Before submitting a pull request:

- [ ] **Tests**: Add or update tests in `tests/`.
  ```bash
  pytest -q
  ```
- [ ] **Type checks**: Ensure code passes `mypy`.
  ```bash
  mypy src
  ```
- [ ] **Lint**: Run `ruff` for style and formatting.
  ```bash
  ruff check src tests
  ```
- [ ] **Docs/examples**: Update README or add an example in `examples/` if relevant.
- [ ] **Commits**: Use clear, descriptive commit messages.

---

## 🧑‍💻 Code Style

- Python ≥ 3.9, fully type-annotated.
- Follow [PEP 8](https://peps.python.org/pep-0008/) and [PEP 484](https://peps.python.org/pep-0484/) type hints.
- Keep modules cohesive (e.g., DFA/NFA logic separate from algorithms).
- Prefer functional clarity over micro-optimizations unless algorithmic efficiency is the point (e.g., Hopcroft’s algorithm).

---

## 📚 Roadmap Ideas

We especially welcome PRs for:

- Automata operations (union, intersection, complement).
- Regex → NFA (Thompson) → DFA (subset).
- Equivalence / inclusion checks.
- Visualization improvements (DOT export, animations).
- Research-oriented features:
  - Angluin’s L* learning algorithm.
  - Symbolic automata for large alphabets.
  - Connections to ML/AI models.

---

## 🤝 Community

- Open an [issue](../../issues) for questions, ideas, or bugs.  
- Tag PRs with the area (`dfa`, `nfa`, `viz`, `docs`).  
- Be respectful and collaborative — we’re building a learning-friendly library together.  

---

## 📖 License

By contributing, you agree that your contributions will be licensed under the MIT License.
