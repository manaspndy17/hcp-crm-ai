import os
os.environ["SSL_CERT_FILE"] = ""
os.environ["CURL_CA_BUNDLE"] = ""

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

from tools import log_interaction, edit_interaction, search_hcp_interactions, schedule_followup, suggest_materials

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

tools = [log_interaction, edit_interaction, search_hcp_interactions, schedule_followup, suggest_materials]

SYSTEM_PROMPT = """You are an AI assistant for field reps in a pharma CRM system.
You help log and edit HCP (Healthcare Professional) interactions using the tools available to you.
Always use the tools to actually save/update data - do not just describe what you would do.
If information is missing (like sentiment), make a reasonable assumption based on the tone of the message.
"""

agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)