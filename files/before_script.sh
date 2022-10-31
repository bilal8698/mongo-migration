#!/bin/bash

# security authentication
mkdir -p /root/.ssh
echo -n $id_rsa_gojek_key | base64 -d > /root/.ssh/id_rsa_gojek_key
chmod 600 /root/.ssh/id_rsa_gojek_key
echo -n $id_rsa_os_login_key | base64 -d > /root/.ssh/id_rsa_os_login_key
chmod 600 /root/.ssh/id_rsa_os_login_key
echo -n $id_rsa_gojek_key_pub | base64 -d > /root/.ssh/id_rsa_gojek_key_pub
chmod 600 /root/.ssh/id_rsa_gojek_key_pub
echo $GOOGLE_APPLICATION_CREDENTIALS | base64 -d > /tmp/service-account.json

# gcloud auth activate-service-account cmp-discovery-automation@systems-0001.iam.gserviceaccount.com --key-file=/tmp/service-account.json --project=systems-0001
gcloud auth activate-service-account discovery-automation@systems-0001.iam.gserviceaccount.com --key-file=/tmp/service-account.json --project=rabbit-hole-integration-007
#gcloud compute os-login ssh-keys add --key-file=/root/.ssh/id_rsa_gojek_key_pub
cp files/run.sh /tmp/ && chmod 755 /tmp/run.sh