#!/bin/bash

echo "$ansibletags"

case "$ansibletags" in
    "setup")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags setup
        ;;
    "validate")
        ansible-playbook  -f 10 -i migration/hosts migration/main.yml --tags validate
        ;;
esac