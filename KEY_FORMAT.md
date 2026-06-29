# API key format (the producer ↔ consumer contract)

Every entry in a snapshot's `keys` array and in `since-index.json` is a **key**: a
string naming one public API element, or one of its parameters. The whole
compatibility check is a string match, so the producer
([knime-python](https://github.com/knime/knime-python) — `scripts/dump_python_api.py`)
and the consumer
([knime-python-bundling](https://github.com/knime/knime-python-bundling) —
`knime/bundling/apicheck.py`, shipped as the `knime-extension-bundling` package)
**must spell keys the same way**. This file is the source of truth for that
spelling. Changing it is a deliberate, coordinated change in both repos.

## Grammar

```
key      := path | path "(" param ")"
path     := root ( "." segment )*
root     := "knime.extension" | "knime.scripting.io"
          | "knime.api.schema" | "knime.api.table"
segment  := Python identifier (dunders allowed, e.g. __init__, __getitem__)
param    := Python identifier (a keyword-argument name)
```

Reference regex (used by the guards on both sides):

```
^(knime\.extension|knime\.scripting\.io|knime\.api\.schema|knime\.api\.table)(\.[A-Za-z_][A-Za-z0-9_]*)*(\([A-Za-z_][A-Za-z0-9_]*\))?$
```

## Examples

| Key | Meaning |
|-----|---------|
| `knime.extension.EnumParameter` | a class |
| `knime.extension.EnumParameter.rule` | a method |
| `knime.extension.BinaryPortObjectSpec.id` | an attribute / property |
| `knime.extension.node(category)` | a parameter of a function / decorator |
| `knime.extension.EnumParameter.__init__(hidden_choices)` | a **constructor** parameter |

## Conventions that must not drift

- **Constructor parameters use `Class.__init__(param)`**, not `Class(param)`. The
  consumer hedges by emitting *both* shapes for every call and matching whichever
  is in the index, but the producer canonically writes `__init__`. Don't
  "simplify" either side away — that would silently stop the two from matching and
  turn the check into a no-op (a false "floor OK").
- **Parameters are the only thing wrapped in `( )`**, and only a single bare
  identifier goes inside. No types, defaults, positions, or `*args`/`**kwargs`.
- **Roots are exactly the four above** — the curated public surface
  (`python_api_pages.yaml` in knime-python). Adding a root is an API-surface change
  that must be made in this grammar, the producer, and the consumer's
  `PUBLIC_API_ROOTS` together.

## What "drift" means

- *Expected change* — new symbols/parameters appear as new keys that still match
  the grammar. No action; the guards pass.
- *Wrongful drift* — the **shape** of keys changes (e.g. dropping `__init__`,
  using `.param` instead of `(param)`, a new root). The grammar guard on each side
  goes red so it's caught before it can silently disable the check.
