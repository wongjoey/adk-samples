import os
from dotenv import load_dotenv
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.tools.apihub_tool.clients.secret_client import SecretManagerClient

from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows


load_dotenv()

CONNECTION_PROJECT_ID=os.getenv("CONNECTOR_0_PROJECT_ID")
CONNECTION_REGION=os.getenv("CONNECTOR_0_CONNECTION_REGION")
CONNECTION_NAME=os.getenv("CONNECTOR_0_CONNECTION_NAME")
APP_AUTH_URL=os.getenv("CONNECTOR_0_AUTH_URL")
APP_TOKEN_URL=os.getenv("CONNECTOR_0_TOKEN_URL")
APP_CLIENT_ID_SM_KEY=os.getenv("CONNECTOR_0_CLIENT_ID_SM_KEY")
APP_CLIENT_SECRET_SM_KEY=os.getenv("CONNECTOR_0_CLIENT_SECRET_SM_KEY")

GCP_SM_APP_CLIENT_ID=f"projects/{CONNECTION_PROJECT_ID}/secrets/{APP_CLIENT_ID_SM_KEY}/versions/latest"
GCP_SM_APP_CLIENT_SECRET=f"projects/{CONNECTION_PROJECT_ID}/secrets/{APP_CLIENT_SECRET_SM_KEY}/versions/latest"

AGENT_REDIRECT_URI=os.getenv("AGENT_REDIRECT_URI")

# Get the credentials for the SaaS App (e.g. Slack)
secret_manager_client = SecretManagerClient()
app_client_id = secret_manager_client.get_secret(GCP_SM_APP_CLIENT_ID)
app_client_secret = secret_manager_client.get_secret(GCP_SM_APP_CLIENT_SECRET)


TOOL_INSTR="""
        **Tool Definition: Slack Connector via Application Integration**

        This toolset interacts with Slack entities (Channels, Messages, Users, UserGroups) using an Application Integration Connector.
        It provides dedicated GET and LIST operations for these entities.

        **General Tool Usage:**

        *   **Tool Naming Convention (Standard Operations):** Dedicated tool functions for Slack entities follow the pattern: `slack_tool_<operation>_<entity_name_singular>`.
            *   Examples: `slack_tool_get_channel`, `slack_tool_list_messages`, `slack_tool_get_user`, `slack_tool_list_usergroups`.
        *   **Supported Standard Entity Operations:**
            *   `Channels`: GET, LIST
            *   `Messages`: GET, LIST
            *   `Users`: GET, LIST
            *   `UserGroups`: GET, LIST

        **Data Retrieval (Standard GET and LIST Operations for Channels, Messages, Users, and UserGroups):**

        *   **Retrieve Specific Record (GET):**
            *   Use the `GET` operation (e.g., `slack_tool_get_channel`, `slack_tool_get_user`).
            *   The `entity_id` parameter **MUST** be the Slack ID of the record (e.g., Channel ID, User ID). For messages, this might be a unique message identifier or timestamp depending on the underlying API.
        *   **Retrieve Multiple Records (LIST):**
            *   Use the `LIST` operation (e.g., `slack_tool_list_messages`, `slack_tool_list_users`).
            *   **Filtering with `filterClause`:** This is essential for targeted data retrieval.
                *   **Filtering Messages (using `slack_tool_list_messages`):**
                    *   To list messages in a specific channel using its ID: `filterClause="channelId='C123ABC456'"`
                    *   To search for messages containing specific text (potentially across all accessible channels, if supported by the connector, or within a specified channel): `filterClause="SearchTerm='your search text'"`
                    *   To search for messages containing specific text within a specific channel: `filterClause="channelId='C123ABC456' AND SearchTerm='your search text'"`
                    *   **If the user provides a channel NAME instead of an ID to list messages:**
                        1. First, use `slack_tool_list_channels` with `filterClause="name='the_channel_name'"` to retrieve the `channelId`.
                        2. Then, use the obtained `channelId` with `slack_tool_list_messages` as shown above (e.g., `filterClause="channelId='C123ABC456'"`).
                    *   If no `filterClause` is provided, it might list messages from all accessible channels or a default set, depending on the connector's behavior.
"""

oauth2_scheme = OAuth2(
   flows=OAuthFlows(
      authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl=APP_AUTH_URL,
            tokenUrl=APP_TOKEN_URL,
            scopes={
                # "admin" : "",
                "channels:read" : "",
                "channels:history" : "",
                # "users.profile:read" : "",
                "users:read" : "",
                "groups:read" : "",
                "im:read" : "",
                "mpim:read" : "",
            }
      )
   )
)

oauth2_credential = AuthCredential(
  auth_type=AuthCredentialTypes.OAUTH2,
  oauth2=OAuth2Auth(
    client_id=app_client_id,
    client_secret=app_client_secret,
    redirect_uri=AGENT_REDIRECT_URI # This is the ADK Web UI
  )
)

integration_connector_tool = ApplicationIntegrationToolset(
    project=CONNECTION_PROJECT_ID, 
    location=CONNECTION_REGION, 
    connection=CONNECTION_NAME,
    tool_name_prefix="slack_tool",
    entity_operations={
        "Messages": ["GET", "LIST"],
        "Channels": ["GET", "LIST"],
        "Users": ["GET", "LIST"],
        "UserGroups": ["GET", "LIST"],
        # "UserProfile": ["GET", "LIST"],
    },
    tool_instructions=TOOL_INSTR,
    auth_credential=oauth2_credential,
    auth_scheme=oauth2_scheme,
)