from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """You are an assistant that extracts structured data from HCP (Healthcare Professional) interaction notes for a pharma CRM.

Extract the following fields from the user's message:
- hcp_name (string)
- interaction_type (string, e.g. "Meeting", "Call", "Email")
- topics_discussed (string, summary of topics)
- sentiment (must be exactly one of: "Positive", "Neutral", "Negative")
- outcomes (string, any agreements or outcomes mentioned, or empty string if none)

Respond with ONLY valid JSON. No preamble, no explanation, no markdown code fences. Just the raw JSON object.

Example output:
{"hcp_name": "Dr. Smith", "interaction_type": "Meeting", "topics_discussed": "Product X efficacy", "sentiment": "Positive", "outcomes": "Agreed to review study data"}
"""

user_input = "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure"

response = llm.invoke([
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input}
])

print("Raw response:", response.content)

# Try parsing it as JSON
try:
    data = json.loads(response.content)
    print("\n✅ Parsed JSON:", data)
    print("HCP Name:", data["hcp_name"])
except json.JSONDecodeError:
    print("\n❌ Failed to parse — model didn't return clean JSON")