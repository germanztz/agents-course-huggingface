from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from langchain_mcp_adapters.tools import to_fastmcp
import pandas as pd
import os

# load environment variables from .env file
load_dotenv()
workfolder = os.getenv('WORKFOLDER')

@tool
def get_emails() -> dict:
    """ Returns the last email received by the system in json: {'from_email':'','to':'','subject':'','body':''}. 
    """
    dummy_emails_df = pd.read_csv(os.path.join(workfolder, "dummy_emails.csv"))
    return dummy_emails_df[['from_email','to','subject','body']].sample(1).iloc[0].to_dict()

@tool 
def get_projects():
    """ Returns the list of the projects in json: [{'tag':'','name':'','description':''}] """
    projects_df = pd.read_csv(os.path.join(workfolder, "projects.csv"))
    return projects_df[['tag','name','description']].to_dict( orient="records")

@tool
def classify_tag_email(email_subject:str, tag_string:str) -> str:
    """ Assigns a tags to an email idenfied by it's subject, with a specific tag. 
    parameters:
    email_subject (str): The subject of the email to tag.
    tag_string (str): The tag to create.
    """
    mail = get_emails.invoke(email_subject)
    mail[tag_name] = tag_value
    print(mail.to_dict())

tools=[
    to_fastmcp(get_emails), 
    to_fastmcp(get_projects), 
    to_fastmcp(classify_tag_email), 
    ]

mcp = FastMCP("mcp", tools=tools)

if __name__ == "__main__":
    mcp.run(transport="stdio")
    # print(get_projects.invoke(''))
    # email = get_emails.invoke('')
    # print(create_tag_email.invoke(email['subject'], 'test'))

