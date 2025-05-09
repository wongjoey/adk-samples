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
    tool_name="snow_connector_tool",
    tool_instructions="""
        **Tool Definition: ServiceNow Connector via Apigee Integration**

        This tool interacts with ServiceNow entities (Problems, Incidents) using an Apigee Integration Connector.
        It supports GET, LIST, and CREATE operations as defined for each entity.

        **CRITICAL: Authentication - `dynamic_auth_config` Parameter**

        *   **MANDATORY:** Every function call to this tool (e.g., `snow_connector_tool_get_problem`, `snow_connector_tool_list_incident`) **MUST** include the `dynamic_auth_config` parameter in the function call.
        *   **SYSTEM HANDLED:** This parameter is automatically populated with the necessary OAuth access token by the system. Your role is to ensure you *always* include `dynamic_auth_config` in your function call requests.
        *   **VALIDATION:** The system expects `dynamic_auth_config` to be present and valid. Do not attempt to generate or modify its value.

        **General Tool Usage:**

        *   **Tool Naming Convention:** Tool functions follow the pattern: `snow_connector_tool_<operation>_<entity_name_singular>`.
            *   Example: `snow_connector_tool_get_problem`, `snow_connector_tool_list_incident`.
        *   **Supported Entity Operations:**
            *   `Problem`: GET, LIST, CREATE
            *   `Incident`: GET, LIST

        **Data Retrieval (GET and LIST Operations):**

        *   **Retrieve Specific Record (GET):**
            *   Use the `GET` operation (e.g., `snow_connector_tool_get_problem`).
            *   The `entity_id` parameter **MUST** be the ServiceNow `sys_id` of the record.
        *   **Retrieve Multiple Records (LIST):**
            *   Use the `LIST` operation (e.g., `snow_connector_tool_list_problem`).
            *   **Filtering with `filterClause`:** This is essential for targeted data retrieval.
                *   **To retrieve a Problem record by its Problem Number (e.g., "PRB000123"):**
                    Use `snow_connector_tool_list_problem` with `filterClause="number='PRB000123'"`.
                *   **To retrieve Problem records assigned to a specific user:**
                    Use `snow_connector_tool_list_problem` with `filterClause="assigned_to='USER_SYS_ID'"` (where `USER_SYS_ID` is the `sys_id` of the user).
                *   **To retrieve related Incidents for a given Problem record:**
                    Use `snow_connector_tool_list_incident` with `filterClause="problem_id='PROBLEM_SYS_ID'"` (where `PROBLEM_SYS_ID` is the `sys_id` of the parent Problem).

        **Problem Creation:**

        *   **Tool:** Use `snow_connector_tool_create_problem`.
        *   **Information Gathering:**
            1.  Collect minimal information from the user to describe the new problem.
            2.  Deduce appropriate values for `category`, `impact`, and `urgency` based on the user-provided details.
        *   **User Confirmation:**
            1.  Before calling `snow_connector_tool_create_problem`, present the summarized details (description, deduced category, impact, urgency) to the user.
            2.  Ask for explicit confirmation from the user to proceed with creation.
        *   **Post-Creation Steps:**
            1.  After the problem is successfully created by `snow_connector_tool_create_problem` (which will return the new record including its `sys_id`).
            2.  Immediately call `snow_connector_tool_get_problem` using the `sys_id` of the newly created problem to fetch its complete and up-to-date details.
            3.  Present the **Problem Number** (e.g., "PRB0040001") and other key details (like description, state, priority) to the user. Do **NOT** show the `sys_id` as the primary identifier to the user.
    """
)