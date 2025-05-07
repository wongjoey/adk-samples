import os
from dotenv import load_dotenv
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

load_dotenv()

PROJECT_ID=os.getenv("PROJECT_ID")
SNOW_CONNECTION_REGION=os.getenv("SNOW_CONNECTION_REGION")
SNOW_CONNECTION_NAME=os.getenv("SNOW_CONNECTION_NAME")


snow_connector_tool = ApplicationIntegrationToolset(
    project=PROJECT_ID, 
    location=SNOW_CONNECTION_REGION, 
    connection=SNOW_CONNECTION_NAME,
    entity_operations={
        "Problem": ["GET", "LIST", "CREATE"],
        "Incident": ["GET", "LIST"],
    },
    # actions=["ExecuteCustomQuery"],
    tool_name="snow_connector_tool",
    tool_instructions="""
        **Tool Definition: ServiceNow Apigee Integration Connector**

        This tool facilitates interaction with ServiceNow through an Apigee Integration Connector.

        **CRITICAL: Dynamic Authentication via `dynamic_auth_config`**

        To ensure secure access, **every** function call to this tool (`snow_connector_tool`) **requires** a `dynamic_auth_config` parameter.

        * **Mandatory Parameter:** Include `dynamic_auth_config` in **all** function calls.
        * **Validation:** The `dynamic_auth_config` parameter **must not** be null, empty, or an empty JSON object (`{}`). It must always contain the valid access token in the specified format.

        **Data Retrieval Considerations:**

        * **Record Identification:** When retrieving specific records using an identifier, use the ServiceNow `sys_id` value for the `entity_id` parameter.
        * **Filtering Related Records:** To retrieve related records when the `sys_id` is unknown (e.g., finding Incidents related to a Problem), use the `LIST` operation with the `filterClause` parameter (e.g., filtering Incidents by `problem_id` which is the parent Problem's `sys_id`).
        * **Retrieving Problem record by Problem Number:** Use LIST operation on Problem entity with filterClause number='`PROBLEM_NUMBER`'.
        * **Retrieving related Incidents for a given Problem record:** Use LIST operation on Incident entity with filterClause problem_id='`sys_id`', where `sys_id` is the parent Problem's `sys_id`.
    """
)