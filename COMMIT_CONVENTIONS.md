# Commit Message Conventions

We use a lightweight version of **Conventional Commits** to keep history readable and automatable.

## Format

```
<type>(<scope>)!: <subject>
<blank line>
<body>
<blank line>
<footer>
```

- **type**: what kind of change (see list below)
- **scope** *(optional)*: area of code (`dfa`, `nfa`, `algorithms`, `io`, `cli`, `docs`, `tests`)
- **!** *(optional)*: indicates a **breaking change**
- **subject**: short summary (imperative mood, ≤ 72 chars)
- **body** *(optional)*: why and what changed; wrap at ~72 chars/line
- **footer** *(optional)*: issue refs (`Fixes #123`), co-authors, BREAKING CHANGE details

## Allowed types

- **feat**: new feature (user-facing API, CLI command)
- **fix**: bug fix
- **perf**: performance improvement
- **refactor**: code change that doesn’t add features or fix bugs
- **docs**: documentation only
- **test**: tests only
- **build**: build system, packaging, dependencies
- **ci**: CI configuration or scripts
- **chore**: repo maintenance (formatting, rename, misc)
- **style**: formatting/whitespace (no code behavior change)

## Examples

**Initial scaffold**
```
chore: initial repository setup

- Add README, LICENSE, CONTRIBUTING
- Add CI (lint, typecheck, test, build)
- Add pre-commit and .gitignore
```

**Feature**
```
feat(algorithms): add Hopcroft DFA minimization
```

**Bug fix**
```
fix(io): preserve state names when exporting DOT
```

**Docs**
```
docs: add Development Setup and pre-commit instructions
```

**Tests**
```
test(minimize): cover sink reachability edge case
```

**Breaking change**
```
refactor(dfa)!: rename `simulate` arg to `input_symbols`

BREAKING CHANGE: simulate() now accepts an iterable of symbols instead of a string.
Update callers accordingly.
```

**Closes an issue**
```
fix(cli): exit with code 1 on REJECT
Fixes #42
```

## Subject style

- Use **imperative mood**: “add”, “fix”, “refactor”, not “added”/“fixes”.
- Keep it **short** (≤ 72 chars), **no period** at the end.
- Avoid noisy words: “update”, “stuff”, “misc”.

## Body guidelines (optional but encouraged)

- Explain **why** the change was needed and **what** changed.
- Mention trade-offs or alternatives considered.
- Include benchmarks if perf-related.
- Wrap lines to ~72 chars.

## Scopes (suggested)

- `dfa`, `nfa`, `regex`, `algorithms`, `io`, `viz`, `cli`, `tests`, `docs`, `build`, `ci`

## Do / Don’t

**Do**
- Group related changes in one commit.
- Keep commits focused and reviewable.
- Reference issues/PRs in the footer.

**Don’t**
- Mix unrelated refactors with features.
- Commit generated artifacts (e.g., `dist/`, `out/*.svg`).
