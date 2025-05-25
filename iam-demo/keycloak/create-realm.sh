#!/bin/bash

/opt/keycloak/bin/kc.sh start-dev &

echo "Waiting for Keycloak to be available..."
until curl -s http://localhost:8080/realms/master; do
  sleep 5
done

/opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# Create Realm
/opt/keycloak/bin/kcadm.sh create realms -s realm=demo-realm -s enabled=true

# Create Client
/opt/keycloak/bin/kcadm.sh create clients -r demo-realm -s clientId=flask-client -s publicClient=true -s directAccessGrantsEnabled=true -s enabled=true

# Create User
/opt/keycloak/bin/kcadm.sh create users -r demo-realm -s username=testuser -s enabled=true
USER_ID=$(/opt/keycloak/bin/kcadm.sh get users -r demo-realm -q username=testuser --fields id --format csv | tail -n 1)
/opt/keycloak/bin/kcadm.sh set-password -r demo-realm --userid "$USER_ID" --new-password testpass