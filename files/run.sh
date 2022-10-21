#!/bin/bash

echo "$ansibletags"

case "$ansibletags" in
    "setup")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags setup
        ;;
    "snapshot")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags snapshot
        ;;
    "restore")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags restore
        ;;
    "verify")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags verify
        ;;
    "status")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags status
        ;;
esac