from google.adk.agents import Agent
from .prompts import ROOT_AGENT_INSTR
# from .sfdc_oauth_tool import sfdc_oauth_tool
from .integration_connector_tool import integration_connector_tool

# from .interceptors import after_tool_run_interceptor # Import the callback function
# from .interceptors import before_tool_run_interceptor # Import the callback function

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='template_agent',
    description="Template Agent.",
    instruction=ROOT_AGENT_INSTR,
    tools= [integration_connector_tool],
)
