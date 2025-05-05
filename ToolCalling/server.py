from mcp.server.fastmcp import FastMCP
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
# Create an MCP server
mcp = FastMCP("AI Sticky Notes")

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")
load_dotenv()

def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")

@mcp.tool()
def clear_note() -> str:
    """
    Clears all the notes from sticky note file

    Returns:
        str: Confirmation message indicating the note was cleared.
    """
    ensure_file()
    with open(NOTES_FILE, "w") as f:
        f.write("")
    return "Notes Cleared!!"

@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky note file.

    Args:
        message (str): The note content to be added.

    Returns:
        str: Confirmation message indicating the note was saved.
    """

    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note saved!"

@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the sticky note file.

    Returns:
        str: All notes as a single string separated by line breaks.
             If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    return content or "No notes yet."

@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the most recently added note from the sticky note file.

    Returns:
        str: The last note entry. If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes yet."

@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all current notes.

    Returns:
        str: A prompt string that includes all notes and asks for a summary.
             If no notes exist, a message will be shown indicating that.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    if not content:
        return "There are no notes yet."

    return f"Summarize the current notes: {content}" 

@mcp.tool()
def send_mail(senderMailId: str, senderPassword: str, 
              recieverMailId: str, subject: str,
              body: str) -> str:

    '''
        Delivers the message from the sender mail to the reciever mail
        Input:
            senderMailId: str -> mail id of the sender
            senderPassword: str -> password of the mail id of sender
            recieverMailId: str -> mail id of the reciever
            subject: str -> subject of the mail
            body: str -> body of the mail
        Output:
            status: str -> status of the process
    '''

    message = MIMEMultipart()
    message["From"] = senderMailId
    message["To"] = recieverMailId
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(senderMailId, senderPassword)
        server.sendmail(senderMailId, recieverMailId, message.as_string())
        server.quit()
        return "Email Send successfully!!"
    except Exception as e:
        return f"Error sending the email : {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
