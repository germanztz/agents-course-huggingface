# Code snippets are only available for the latest version. Current version is 1.x
from msgraph import GraphServiceClient
# To initialize your graph_client, see https://learn.microsoft.com/en-us/graph/sdks/create-client?from=snippets&tabs=python

from langchain_core.tools import tool

@tool
def get_messages() -> str:

    scopes = ['User.Read']

    # Multi-tenant apps can use "common",
    # single-tenant apps must use the tenant ID from the Azure portal
    tenant_id = 'common'

    # Values from app registration
    client_id = 'YOUR_CLIENT_ID'

    # azure.identity
    credential = DeviceCodeCredential(
        tenant_id=tenant_id,
        client_id=client_id)

    graph_client = GraphServiceClient(credential, scopes)

    result = await graph_client.me.messages.get()
    return result
