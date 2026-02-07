#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXECUTABLE="$ROOT_DIR/src/dist/bibliotecaTK"

if [[ ! -x "$EXECUTABLE" ]]; then
  echo "No se encontró ejecutable en: $EXECUTABLE"
  echo "Compila primero con: (cd src && pipenv run pyinstaller bibliotecaTK.spec)"
  exit 1
fi

exec "$EXECUTABLE" "$@"
