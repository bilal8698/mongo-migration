#!/bin/bash

echo "$ansibletags"

case "$ansibletags" in
    "setup")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags setup
        ;;
    "status")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags status
        ;;
    "cutover")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags cutover
        ;;
    "validate")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags validate
        ;;
    "rollback")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags rollback
        ;;
esac
