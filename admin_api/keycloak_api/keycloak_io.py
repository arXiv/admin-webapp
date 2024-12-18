import json
import logging
import os
from typing import Optional

from keycloak import KeycloakAdmin, KeycloakError
import argparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class KeycloakUp(KeycloakAdmin):

    def __init__(self, *args, **kwargs):
        self.realm = kwargs.pop('realm')
        super().__init__(*args, **kwargs)


    def restore_roles(self):
        existing_roles = {role['name']: role for role in self.get_realm_roles()}

        realm_roles = self.realm['roles']['realm']
        # Define Role Data
        for role in realm_roles:
            role_name = role['name']
            if role_name[0].upper() != role_name[0]:
                continue
            if role_name in existing_roles:
                continue
            role_description = role['description']
            self.create_realm_role(
                payload={
                    "name": role_name,
                    "description": role_description
                }
            )


    def restore_scopes(self):
        existing_scopes = {scope['name'] for scope in self.get_client_scopes()}
        realm_scopes = self.realm['clientScopes']

        for scope in realm_scopes:
            if scope['name'] in existing_scopes:
                continue

            try:
                # Create the 'openid' scope
                payload = scope.copy()
                del payload['id']
                scope_id = self.create_client_scope(payload=payload, skip_exists=True)
                logger.info(f"Scope '{payload["name"]}' created successfully. {scope_id}")

            except KeycloakError as exc:
                logger.error(f"Error creating {payload['name']}: {exc}")


    def restore_client(self, client_id: str):
        target: Optional[dict] = next((client for client in self.realm['clients'] if client['clientId'] == client_id), None)
        if not target:
            logger.error(f"Client '{client_id}' not found.")
            return

        payload = target.copy()
        del payload['id']
        del payload['secret']
        del payload['attributes']["client.secret.creation.time"]
        del payload['protocolMappers']



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--realm', type=str, default='arxiv')
    parser.add_argument('--server', type=str, default=os.environ.get("KEYCLOAK_SERVER_URL", 'http://localhost:3033'))
    parser.add_argument('--secret', type=str, default='')

    args = parser.parse_args()

    with open(os.path.expanduser("~/arxiv/arxiv-auth/keycloak_bend/realms/arxiv-realm.json")) as realm_fd:
        realm = json.load(realm_fd)


    secret = args.secret
    if not secret:
        with open(os.path.expanduser("~/.arxiv/keycloak-admin-password-dev"), encoding="utf-8") as fd:
            secret = fd.read().strip()

    admin = KeycloakUp(
        realm=realm,
        server_url=args.server,
        user_realm_name="master",
        client_id="admin-cli",
        username="admin",
        password=secret,
        realm_name=args.realm,
        verify=False,
    )

    admin.restore_roles()
    admin.restore_scopes()
    admin.restore_client("arxiv-user")
