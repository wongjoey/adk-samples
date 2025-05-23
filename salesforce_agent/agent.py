from google.adk.agents import Agent
from .prompts import ROOT_AGENT_INSTR
from .sfdc_connector_tool import sfdc_connector_tool

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='salesforce_agent',
    description="SalesForce Agent to get details on accounts and contacts.",
    instruction=ROOT_AGENT_INSTR,
    tools= [sfdc_connector_tool],
)
