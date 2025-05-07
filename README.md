# adk-samples

**Installation**
 * python -m venv .venv
 * source .venv/bin/activate
 * pip install google-adk

**Update configs**
 * .env
 * snow_connector_tool.py
 * snow_oauth_tool.py
 * snow_oauth_tool_apihub.py
 * update snow_spec_v2.yaml to point to your own ServiceNow instance

**Pre-Reqs**
 * Create entries for `adk-snow-client-id` and `adk-snow-client-secret` in Google Cloud Secrets Manager
 * Create ServiceNow connection (assumes that you have ServiceNow also setup to use OAuth), update the connection name as required.
 * If planning to use API hub, make sure you register the ServiceNow API and upload the `snow_spec_v2.yaml`. The sample code assumes that the entity-id is `servicenow-api`, you will have to replace this if you use another id or if you let the platform generate it for you. 

**Details**
 * snow_connector_tool.py - Uses Integration Connectors
 * snow_oauth_tool.py - Uses given OAS spec to build tool to facilitate OAuth flow.
 * snow_oauth_tool_apihub.py - Uses given OAS spec (stored in API hub) to build tool to facilitate OAuth flow.

**Important**
 * The current version of ADK for Integration Connectors is not passing the dynamic auth config to override the token used by the connection. As a workaround I've manually added the dynamicAuthConfig object to connections_client.py. There is an open FR and PR that will fix this. See:
   * [FR: Support Dynamic Auth Config for Integration Connectors tool. #464
](https://github.com/google/adk-python/issues/464)
   * [PR: feat(application-integration-tool): add dynamic authentication configuration support #469](https://github.com/google/adk-python/pull/469)