# Purpose

This is a template project to quickly build a new agent using ADK + Application Integration (Connectors).

## Pre-requisites

* Appropriate GCP APIs enabled
* Applicaition Integration setup correctly
* Integration Connector setup correctly
* Client ID and Secrets are setup correctly for your target application
* ADK (Agent Development Kit) installed and configured

## Configuration updates

Make a copy of `.env_template` and name it `.env`

Majority of the configurations are in the `.env` file. Please look in there and replace all the values to match your configured Application Integration and Integration Connector setup.

## Additional updates

Tweak the `prompts.py` and `integration_connector_tool.py` instructions to match your use case.
