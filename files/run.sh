#!/bin/bash
set -eo pipefail

# Validate input
if [[ -z "$1" ]]; then
    echo "Usage: $0 <step>"
    echo "Available steps: setup, validate, cutover, datavalidate, rollback"
    exit 1
fi

STEP=$1
LOG_FILE="/var/log/mongo-migration-$(date +%Y%m%d-%H%M%S).log"

echo "[$(date)] Starting migration step: $STEP" | tee -a "$LOG_FILE"

case "$STEP" in
    "setup")
        ansible-playbook -i migration/hosts migration/main.yml --tags setup
        ;;
    "validate")
        ansible-playbook -i migration/hosts migration/main.yml --tags validate
        ;;
    "cutover")
        ansible-playbook -i migration/hosts migration/main.yml --tags cutover
        ;;
    "datavalidate")
        ansible-playbook -i migration/hosts migration/main.yml --tags datavalidate
        ;;
    "rollback")
        ansible-playbook -i migration/hosts migration/main.yml --tags rollback
        ;;
    *)
        echo "ERROR: Unknown step: $STEP" | tee -a "$LOG_FILE"
        exit 1
        ;;
esac

echo "[$(date)] Completed migration step: $STEP" | tee -a "$LOG_FILE"