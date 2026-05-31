#!/usr/bin/env bash
# verify.sh — Check that all infrastructure services are reachable.
#
# Usage:
#   ./scripts/verify.sh
#
# Prerequisites:
#   - docker compose services running (docker compose -f docker/docker-compose.yml up -d)
#   - psql, redis-cli  (optional — falls back to TCP checks)

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

check_service() {
  local name="$1"
  local host="$2"
  local port="$3"

  printf "  %-12s " "$name"

  # Try a simple TCP connection (works on Linux & macOS)
  if command -v nc &>/dev/null; then
    if nc -z -w 3 "$host" "$port" 2>/dev/null; then
      echo -e "${GREEN}OK${NC}  (port $port)"
      ((PASS++))
      return
    fi
  elif command -v bash &>/dev/null; then
    # Fallback: bash /dev/tcp
    if (echo >/dev/tcp/"$host"/"$port") 2>/dev/null; then
      echo -e "${GREEN}OK${NC}  (port $port)"
      ((PASS++))
      return
    fi
  fi

  echo -e "${RED}FAIL${NC}  (port $port not reachable)"
  ((FAIL++))
}

echo ""
echo -e "${YELLOW}🔍 Portfolio Analyzer — Infrastructure Health Check${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── PostgreSQL ───────────────────────────────────────────
check_service "PostgreSQL" "localhost" 5432

# ── Redis ────────────────────────────────────────────────
check_service "Redis" "localhost" 6379

# ── Qdrant ───────────────────────────────────────────────
check_service "Qdrant" "localhost" 6333

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  Results:  ${GREEN}$PASS passed${NC}  /  ${RED}$FAIL failed${NC}"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo -e "${RED}✗ Some services are not reachable.${NC}"
  echo "  Make sure Docker Compose is running:"
  echo "    docker compose -f docker/docker-compose.yml up -d"
  exit 1
else
  echo -e "${GREEN}✓ All services are healthy!${NC}"
  exit 0
fi
