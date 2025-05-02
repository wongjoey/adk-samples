from google.adk.agents import Agent
from .prompts import ROOT_AGENT_INSTR
from .snow_oauth_tool import snow_api_tool
# from .snow_oauth_tool_apihub import snow_api_tool
from .snow_connector_tool import snow_connector_tool
from .interceptors import after_tool_run_interceptor # Import the callback function
from .interceptors import before_tool_run_interceptor # Import the callback function

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='my_test_agent_2',
    description="The agent must first authenticate the end user and be authorized to access ServiceNow using the `snow_api_tool`. After authenticating using the `snow_api_tool`, let the use know if it was successful or not. For all other actions use the `snow_connector_tool`.",
    instruction=ROOT_AGENT_INSTR,
    tools= snow_api_tool.get_tools() + snow_connector_tool.get_tools(),
    after_tool_callback=after_tool_run_interceptor,
    before_tool_callback=before_tool_run_interceptor,
)
