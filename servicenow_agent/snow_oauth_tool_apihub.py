from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth

from google.adk.tools.apihub_tool.apihub_toolset import APIHubToolset
from google.adk.tools.apihub_tool.clients.secret_client import SecretManagerClient

from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows

PROJECT_ID="CHANGE_ME"
APIHUB_LOCATION="CHANGE_ME"
SNOW_INSTANCE_NAME="CHANGE_ME"
SNOW_OAUTH_SCOPES="useraccount"
REDIRECT_URI="http://localhost:8000/dev-ui"
API_HUB_LOCATION=f"projects/{PROJECT_ID}/locations/{APIHUB_LOCATION}/apis"
SNOW_CLIENT_ID=f"projects/{PROJECT_ID}/secrets/adk-snow-client-id/versions/latest"
SNOW_CLIENT_SECRET=f"projects/{PROJECT_ID}/secrets/adk-snow-client-secret/versions/latest"

# Get the credentials for the ServiceNow APIs
secret_manager_client = SecretManagerClient()
snow_client_id = secret_manager_client.get_secret(SNOW_CLIENT_ID)
snow_client_secret = secret_manager_client.get_secret(SNOW_CLIENT_SECRET)

auth_scheme = OAuth2(
   flows=OAuthFlows(
      authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl=f"https://{SNOW_INSTANCE_NAME}.service-now.com/oauth_auth.do",
            tokenUrl=f"https://{SNOW_INSTANCE_NAME}.service-now.com/oauth_token.do",
            scopes={
                f"{SNOW_OAUTH_SCOPES}" : "useraccount",
            }
      )
   )
)

auth_credential = AuthCredential(
  auth_type=AuthCredentialTypes.OAUTH2,
  oauth2=OAuth2Auth(
    client_id=snow_client_id,
    client_secret=snow_client_secret,
    redirect_uri=f"{REDIRECT_URI}" # This is the ADK Web UI
  )
)

snow_api_tool = APIHubToolset(
   name="servicenow-api",
   description="ServiceNow API",
   apihub_resource_name=f"{API_HUB_LOCATION}/servicenow-api",
   auth_scheme=auth_scheme,
   auth_credential=auth_credential,
)
