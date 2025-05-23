import os
from dotenv import load_dotenv
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.tools.apihub_tool.clients.secret_client import SecretManagerClient

from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows


load_dotenv()

CONNECTION_PROJECT_ID=os.getenv("SFDC_CONNECTION_PROJECT_ID")
CONNECTION_REGION=os.getenv("SFDC_CONNECTION_REGION")
CONNECTION_NAME=os.getenv("SFDC_CONNECTION_NAME")

APP_AUTH_URL=os.getenv("SFDC_AUTH_URL")
APP_TOKEN_URL=os.getenv("SFDC_TOKEN_URL")

AGENT_REDIRECT_URI=os.getenv("AGENT_REDIRECT_URI")

GCP_SM_APP_CLIENT_ID=f"projects/{CONNECTION_PROJECT_ID}/secrets/adk-sfdc-client-id/versions/latest"
GCP_SM_APP_CLIENT_SECRET=f"projects/{CONNECTION_PROJECT_ID}/secrets/adk-sfdc-client-secret/versions/latest"

# Get the credentials for the SaaS App (e.g. SFDC)
secret_manager_client = SecretManagerClient()
app_client_id = secret_manager_client.get_secret(GCP_SM_APP_CLIENT_ID)
app_client_secret = secret_manager_client.get_secret(GCP_SM_APP_CLIENT_SECRET)


TOOL_INSTR="""
        **Tool Definition: Salesforce CRM Connector via Apigee Integration**

        This toolset interacts with Salesforce CRM entities using an Apigee Integration Connector.
        It provides dedicated GET, LIST, and CREATE operations for Account, Contact, and Case entities.
        For retrieving data from any other Salesforce entities, or for complex queries on Account, Contact, or Case not covered by the standard LIST operations, the `ExecuteCustomQuery` action **MUST** be used.
        Note: CREATE is currently only supported for Case entities via the standard operations.

        **General Tool Usage:**

        *   **Tool Naming Convention (Standard Operations):** Dedicated tool functions for Account and Contact follow the pattern: `sfdc_tool_<operation>_<entity_name_singular>`.
            *   Example: `sfdc_tool_get_account`, `sfdc_tool_list_contact`.
        *   **Supported Standard Entity Operations:**
            *   `Account`: GET, LIST (Use `sfdc_tool_get_account`, `sfdc_tool_list_account`)
            *   `Contact`: GET, LIST (Use `sfdc_tool_get_contact`, `sfdc_tool_list_contact`)
            *   `Case`: GET, LIST, CREATE (Use `sfdc_tool_get_case`, `sfdc_tool_list_case`, `sfdc_tool_create_case`)

        **Data Retrieval (Standard GET and LIST Operations for Account, Contact, and Case):**

        *   **Retrieve Specific Record (GET):**
            *   Use the `GET` operation (e.g., `sfdc_tool_get_account`, `sfdc_tool_get_contact`, `sfdc_tool_get_case`).
            *   The `entity_id` parameter **MUST** be the SalesForce CRM `id` of the record.
        *   **Retrieve Multiple Records (LIST):**
            *   Use the `LIST` operation (e.g., `sfdc_tool_list_account`, `sfdc_tool_list_contact`, `sfdc_tool_list_case`).
            *   **Filtering with `filterClause`:** This is essential for targeted data retrieval.
                *   Example: To retrieve Cases related to a specific Account, use `sfdc_tool_list_case` with `filterClause="AccountId='ACCOUNT_ID'"`.
                *   Example: To retrieve Cases with a specific status, use `sfdc_tool_list_case` with `filterClause="Status='New'"`.
                *   **Default Filter for Sorting/Limiting:** If you need to apply sorting (ORDER BY) or limiting (LIMIT) but don't have specific field filters from the user, start your `filterClause` with `1=1`. For example, to list all Accounts and order them by Name, you could use `filterClause="1=1 ORDER BY Name ASC --"`.
                *   **Sorting Results:** To sort the retrieved records, append an `ORDER BY` clause to your filter. For example, to get the 50 most recent Cases sorted by their creation date in descending order, you could use: `filterClause="Status='New' ORDER BY CreatedDate DESC LIMIT 50 --"`. Remember to use SOQL-compatible field names and syntax. The `--` at the end is a SOQL comment to ensure any unintentionally appended text by the model does not break the query. Always include it when using `ORDER BY`.

        **Case Creation (Using `sfdc_tool_create_case`):**

        *   **Tool:** Use `sfdc_tool_create_case`.
        *   **Information Gathering:** Collect necessary information from the user to create the case (e.g., Subject, Description, Origin, Status, Priority, related AccountId or ContactId if known).
        *   **User Confirmation:** It is good practice to summarize the details you plan to use for creation and ask for user confirmation *before* calling the tool.
        *   **Post-Creation Steps:** After successful creation, the tool will return the new Case record, including its `Id`. You should then present the Case Number and other relevant details to the user.

        **Custom Data Retrieval (Using `sfdc_tool_execute_custom_query`):**

        *   **When to Use `sfdc_tool_execute_custom_query`:**
            *   When you need to retrieve data from any Salesforce entity **other than** Account or Contact (e.g., Opportunity, Lead, Case, etc.).
            *   When performing complex queries on Account or Contact that cannot be achieved with the standard `LIST` operation's `filterClause`.
            *   When the user explicitly provides a SOQL query or asks for information that clearly requires a custom SOQL query.
        *   **How to Use `sfdc_tool_execute_custom_query`:**
            *   You are an expert in SOQL. Formulate the appropriate SOQL query based on the user's request.
            *   Call the `sfdc_tool_execute_custom_query` action with the formulated SOQL query in the `query` parameter.
"""

oauth2_scheme = OAuth2(
   flows=OAuthFlows(
      authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl=APP_AUTH_URL,
            tokenUrl=APP_TOKEN_URL,
            scopes={
                "full" : "everything",
                "id" : "id",
                "openid" : "openid",
                "profile" : "profile",
                "email" : "email"
            }
      )
   )
)

oauth2_credential = AuthCredential(
  auth_type=AuthCredentialTypes.OAUTH2,
  oauth2=OAuth2Auth(
    client_id=app_client_id,
    client_secret=app_client_secret,
    redirect_uri=AGENT_REDIRECT_URI
  )
)

sfdc_connector_tool = ApplicationIntegrationToolset(
    project=CONNECTION_PROJECT_ID, 
    location=CONNECTION_REGION, 
    connection=CONNECTION_NAME,
    tool_name_prefix="sfdc_tool",
    entity_operations={
        "Account": ["GET", "LIST"],
        "Contact": ["GET", "LIST"],
        "Case": ["GET", "LIST", "CREATE"],
    },
    actions=["ExecuteCustomQuery"],
    tool_instructions=TOOL_INSTR,
    auth_credential=oauth2_credential,
    auth_scheme=oauth2_scheme,
)