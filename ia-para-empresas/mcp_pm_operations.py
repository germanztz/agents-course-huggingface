from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from langchain_mcp_adapters.tools import to_fastmcp
import pandas as pd
import os
import json

# load environment variables from .env file
load_dotenv()
workfolder = os.getenv('WORKFOLDER')
projects_df = pd.read_csv(os.path.join(workfolder, "projects.csv"))
email_reasons_df = pd.read_csv(os.path.join(workfolder, "email_reasons.csv"))

@tool
def send_email(from_email:str, to_email:str, subject:str, body:str) -> str:
    """ Sends an email. 
    parameters:
    from_email (str): The sender's email address.
    to_email (str): The recipient's email address.
    subject (str): The subject of the email.
    body (str): The body of the email.
    """
    try:
        email = {'from_email': from_email, 'to_email': to_email, 'subject': subject, 'body': body, 'tags': ''}
        file_path = os.path.join(workfolder, "emails.csv")
        if os.path.exists(file_path):
            emails_df = pd.read_csv(file_path, index_col='id')
            emails_df = pd.concat([emails_df, pd.DataFrame([email])], ignore_index=True)
            print(file_path)
        else:
            emails_df = pd.DataFrame([email])

        emails_df.to_csv(file_path, index=True, index_label='id')
        return "email sent successfully"
    except Exception as e:
       return f"email sending failed {e}"

@tool
def get_emails() -> dict:
    """ Returns the last email received by the system with empty tags, in json: {'id': 0, 'from_email': '', 'to_email': '', 'subject': '', 'body': '', 'tags': ''}.
    If no emails with empty tags are found, returns a no new message error.
    """
    emails_df = pd.read_csv(os.path.join(workfolder, "emails.csv"), index_col='id')

    # Filter for emails with empty or NaN tags
    emails_without_tags = emails_df[emails_df['tags'].isnull() | (~emails_df['tags'].fillna('').str.contains(','))]

    if not emails_without_tags.empty:
        return emails_without_tags.fillna('').reset_index().sample(1).iloc[0].to_dict()
    else:
        return "No new messages"

@tool 
def get_projects() -> dict:
    """ Returns the list of the projects, in json: [{'tag':'','name':'','description':''}] """
    return projects_df[['tag','name','description']].to_dict( orient="records")

@tool
def modify_email(email_id: int, tag_string: str) -> str:
    """ Modifies an email identified by its ID, adding a tag to it.
    parameters:
    email_id (int): The ID of the email to tag.
    tag_string (str): The tag to create.
    """
    try:
        emails_df = pd.read_csv(os.path.join(workfolder, "emails.csv"), index_col='id')
        tags = emails_df.at[email_id, 'tags'] if pd.notna(emails_df.at[email_id, 'tags']) else ''
        tags = tags.split(',') if len(tags) > 1 else []
        tags.append(tag_string)
        tags.append(tag_string)
        tags = list(set(tags))
        tags = ','.join(tags)
        emails_df.at[email_id, 'tags'] = str(tags)
        emails_df.to_csv(os.path.join(workfolder, "emails.csv"), index=True, index_label='id')
        return f"email {email_id} updated successfully with tag {tag_string}"
    except Exception as e:
        return f"email modifying failed {e}"

@tool
def get_reasons() -> dict:
    """ Returns the list of reasons for sending an email, in json: [{ 'reason':'','description':'','action':'' }]. 
    """
    return email_reasons_df.to_dict(orient="records")

tools=[
    to_fastmcp(get_emails), 
    to_fastmcp(get_projects), 
    to_fastmcp(get_reasons), 
    to_fastmcp(modify_email), 
    to_fastmcp(send_email), 
    ]

mcp = FastMCP("mcp", tools=tools)

if __name__ == "__main__":
    mcp.run(transport="stdio")


    # print(get_projects.invoke(''))
    # print(get_reasons.invoke(''))
    # print('send_email:', send_email.invoke(input={"from_email":"admin@example.com", "to_email":"user@example.com", "subject":"Test Subject", "body":"This is a test email"}))
    # email = get_emails.invoke('')
    # print('get_emails:', email)
    # print('modify_email:', modify_email.invoke(input={"email_id":email['id'], "tag_string":"test"}))
    # print('get_emails:', get_emails.invoke(''))
    # print(modify_email.invoke(input={"email_id":email['id'], "tag_string":"tag2"}))
    # print(modify_email.invoke(input={"email_id":email['id'], "tag_string":"tag3"}))

