import os
from dotenv import load_dotenv

from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth

from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.tools.apihub_tool.clients.secret_client import SecretManagerClient


from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows

load_dotenv()

with open(os.path.join(os.path.dirname(__file__), 'snow_spec_v2.yaml'), 'r') as f:
    content = f.read()

PROJECT_ID=os.getenv("PROJECT_ID")
SNOW_INSTANCE_NAME=os.getenv("SNOW_INSTANCE_NAME")
SNOW_OAUTH_SCOPES=os.getenv("SNOW_OAUTH_SCOPES")
REDIRECT_URI=os.getenv("REDIRECT_URI")
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
                f"{SNOW_OAUTH_SCOPES}" : "default",
            }
      )
   )
)

auth_credential = AuthCredential(
  auth_type=AuthCredentialTypes.OAUTH2,
  oauth2=OAuth2Auth(
    client_id=snow_client_id,
    client_secret=snow_client_secret,
    redirect_uri=REDIRECT_URI # This is the ADK Web UI
  )
)

snow_api_tool = OpenAPIToolset(
   spec_str=content, # Fill this with an openapi spec
   spec_str_type='yaml',
   auth_scheme=auth_scheme,
   auth_credential=auth_credential,
)