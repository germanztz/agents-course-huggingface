import pandas as pd
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
import os

workfolder = os.getenv('WORKFOLDER')

@tool
def get_mails():
    """ Returns a dict with {'from_email','to','subject','body'} of the last email received by the system. 
    """
    dummy_emails_df = pd.read_csv(os.path.join(workfolder, "dummy_emails.csv"))
    return dummy_emails_df[['from_email','to','subject','body']].sample(1).iloc[0].to_dict()

@tool 
def get_projects():
    """ Returns a list of dict {'tag','name','description'} of all the projects. """
    projects_df = pd.read_csv(os.path.join(workfolder, "projects.csv"))
    return projects_df[['tag','name','description']].to_dict( orient="records")

@tool
def tag_mail(subject, tag_name, tag_value):
    """ Tags a mail with a specific tag. 
    parameters:
    subject (str): The subject of the mail to tag.
    tag_name (str): The name of the tag to create. [project or reason]
    tag_value (str): The value of the tag
    """
    mail = get_mails(subject)
    mail[tag_name] = tag_value
    print(mail.to_dict())

tools = {
    "get_mails": get_mails,
    "get_projects": get_projects,
    "tag_mail": tag_mail,
}

mcp = FastMCP(tools)

if __name__ == "__main__":
    # Example usage (for testing purposes)
    print("Starting MCP server...")
    mcp.run() # blocking
    print("MCP server stopped.")
