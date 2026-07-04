"""CLI de validação do catálogo de agentes.

Uso:
    python3 -m wss13_gos.validate_catalog [caminho_do_csv]

Padrão: ../registers/catalogo-agentes.csv (relativo a impl/).
Sai com código 1 se algum agente REGISTRADO falhar na validação.
"""

from __future__ import annotations

import os
import sys

from .agent_catalog import validate_catalog

DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "registers", "catalogo-agentes.csv"
)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    path = argv[0] if argv else DEFAULT_PATH
    if not os.path.exists(path):
        print(f"arquivo não encontrado: {path}", file=sys.stderr)
        return 2
    report = validate_catalog(path)
    print(report.summary())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
