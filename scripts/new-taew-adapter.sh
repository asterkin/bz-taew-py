#!/usr/bin/env bash
set -euo pipefail

# Scaffolds a new taew adapter sub-project from project-template
# Supports locations:
#   - python/<lib>/<port>
#   - python/ram/<port>
#   - <tech>/<port>
# Usage examples:
#   scripts/new-taew-adapter.sh --tech python --lib zlib --port for_transforming_bytes --desc "Zlib bytes transform adapter"
#   scripts/new-taew-adapter.sh --tech python --lib ram --port for_storing_data --desc "RAM store adapter"
#   scripts/new-taew-adapter.sh --tech launch_time --port for_binding_interfaces --desc "Launch time DI adapter"

TECH=""
LIB=""
PORT=""
DESC=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tech) TECH="$2"; shift 2 ;;
    --lib) LIB="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --desc) DESC="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 --tech <tech> [--lib <lib>] --port <port> [--desc <description>]"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$TECH" || -z "$PORT" ]]; then
  echo "--tech and --port are required" >&2
  exit 1
fi

# Determine location path
if [[ "$TECH" == "python" && -n "$LIB" ]]; then
  LOCATION="python/$LIB/$PORT"
else
  LOCATION="$TECH/$PORT"
fi

# Compute project name
if [[ "$TECH" == "python" && -n "$LIB" ]]; then
  PROJECT_NAME="taew.adapters.$TECH.$LIB.$PORT"
else
  PROJECT_NAME="taew.adapters.$TECH.$PORT"
fi

# Determine relative path to core from LOCATION
IFS='/' read -r -a parts <<< "$LOCATION"
depth=${#parts[@]}
# repo root is one level above first directory; core is at root/core
rel=".."
for ((i=1;i<depth;i++)); do rel="${rel}/.."; done
REL_CORE_PATH="$rel/core"

# Author info
AUTHOR_NAME=$(git config user.name || echo "Your Name")
AUTHOR_EMAIL=$(git config user.email || echo "your@email")

# Create directory and copy template
mkdir -p "$LOCATION"
cp -r project-template/* "$LOCATION/"

# Adjust pyproject.toml placeholders and core paths
PP="$LOCATION/pyproject.toml"
sed -i.bak \
  -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
  -e "s/{{PROJECT_DESCRIPTION}}/${DESC//\//\/}/g" \
  -e "s/{{AUTHOR_NAME}}/${AUTHOR_NAME//\//\/}/g" \
  -e "s/{{AUTHOR_EMAIL}}/${AUTHOR_EMAIL//\//\/}/g" \
  "$PP"

# Replace default ../core with computed path in three places
sed -i.bak \
  -e "s#\"\../core\"#\"$REL_CORE_PATH\"#g" \
  "$PP"

rm -f "$PP.bak"

# Create adapter package directories (namespace rules)
if [[ "$TECH" == "python" && -n "$LIB" ]]; then
  PKG_DIR="$LOCATION/taew/adapters/$TECH/$LIB/$PORT"
else
  PKG_DIR="$LOCATION/taew/adapters/$TECH/$PORT"
fi
mkdir -p "$PKG_DIR"
touch "$PKG_DIR/__init__.py"

# Create test skeleton with __init__.py in each folder
TEST_DIR_BASE="$LOCATION/test/test_adapters"
if [[ "$TECH" == "python" && -n "$LIB" ]]; then
  TEST_DIR="$TEST_DIR_BASE/test_$TECH/test_$LIB/test_$PORT"
else
  TEST_DIR="$TEST_DIR_BASE/test_$TECH/test_$PORT"
fi
mkdir -p "$TEST_DIR"
python - "$TEST_DIR" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
for parent in (p.parent.parent.parent, p.parent.parent, p.parent, p):
    if parent and parent.exists():
        (parent/"__init__.py").touch()
PY

echo "Scaffolded $PROJECT_NAME at $LOCATION"
