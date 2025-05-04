#!/bin/bash
set -eo pipefail

# Setup secure environment
umask 077
TEMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TEMP_DIR"
    rm -f /root/.ssh/id_rsa_*
    rm -f /tmp/service-account.json
}
trap cleanup EXIT

# Security authentication
echo -n "$id_rsa_gojek_key" | base64 -d > "$TEMP_DIR/id_rsa_gojek_key"
echo -n "$id_rsa_os_login_key" | base64 -d > "$TEMP_DIR/id_rsa_os_login_key"
echo -n "$id_rsa_gojek_key_pub" | base64 -d > "$TEMP_DIR/id_rsa_gojek_key_pub"
echo "$GOOGLE_APPLICATION_CREDENTIALS" | base64 -d > "$TEMP_DIR/service-account.json"

# Validate keys
if ! ssh-keygen -y -f "$TEMP_DIR/id_rsa_gojek_key" | diff - "$TEMP_DIR/id_rsa_gojek_key_pub"; then
    echo "ERROR: Key validation failed" >&2
    exit 1
fi

# GCP authentication
gcloud auth activate-service-account \
    --key-file="$TEMP_DIR/service-account.json" \
    --project=rabbit-hole-integration-007

# Prepare scripts
cp files/run.sh /tmp/ && chmod 755 /tmp/run.sh