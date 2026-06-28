import os
from google import genai
from google.genai import types

# Initialize the Gemini Client (uses your $env:GEMINI_API_KEY)
client = genai.Client()


# ==========================================
# 🤖 DEFINING AGENT PERSONAS & INSTRUCTIONS
# ==========================================
ROUTER_SYSTEM_INSTRUCTION = """
You are the Orchestrator/Router Agent. Your sole job is to analyze incoming user requests and route them to the correct specialist.
Available Specialists:
1. DOCUMENTATION_AGENT: Use this if the user is asking for technical definitions, API schemas, or docs.
2. COMPLIANCE_AGENT: Use this if the user wants to log, parse, or audit a monetary expense receipt.

Your response must ONLY be the name of the specialist agent. Do not add any conversational text.
"""

DOCS_SYSTEM_INSTRUCTION = """
You are the Technical Documentation Specialist. You are connected to an external MCP knowledge base.
Provide deep, accurate technical details regarding API schemas or engineering specifications.
"""

COMPLIANCE_SYSTEM_INSTRUCTION = """
You are the Financial Compliance Agent. You process expense data strictly. 
Ensure you validate fields and always alert the system if an anomaly or high-value charge occurs.
"""


# ==========================================
# 🚀 CORE ORCHESTRATION PIPELINE
# ==========================================
def run_multi_agent_pipeline(user_prompt: str):
    print(f"\n📥 [User Input Received]: '{user_prompt}'")
    print("🧠 [Router Agent]: Analyzing routing topology...")

    # 1. Route the request using an isolated classification turn
    router_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=ROUTER_SYSTEM_INSTRUCTION,
            temperature=0.0,
        ),
    )

    assigned_agent = router_response.text.strip()
    print(f"🔀 [Router Agent]: Handing off execution context to -> {assigned_agent}")

    # 2. Stateful Handoff Execution
    if "DOCUMENTATION_AGENT" in assigned_agent:
        # Initialize a stateful multi-turn chat session for the Docs Agent
        chat_session = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=DOCS_SYSTEM_INSTRUCTION, temperature=0.2
            ),
        )
        response = chat_session.send_message(user_prompt)
        print(f"\n🤖 [Docs Agent Response]:\n{response.text}")

    elif "COMPLIANCE_AGENT" in assigned_agent:
        # Initialize a stateful multi-turn chat session for the Compliance Agent
        chat_session = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=COMPLIANCE_SYSTEM_INSTRUCTION,
                temperature=0.0,
            ),
        )
        response = chat_session.send_message(user_prompt)
        print(f"\n🤖 [Compliance Agent Response]:\n{response.text}")

    else:
        print(
            f"⚠️ Handoff Failed: Unknown routing target '{assigned_agent}'. Falling back to default assistant."
        )


# ==========================================
# 🧪 TEST MATRICES
# ==========================================
if __name__ == "__main__":
    # Test Turn 1: Should trigger the Compliance Agent
    run_multi_agent_pipeline(
        "Can you log a business receipt? I spent $350.00 on hotel accommodation during the tech conference last week."
    )

    print("=" * 60)

    # Test Turn 2: Should trigger the Documentation Agent
    run_multi_agent_pipeline(
        "What is the strict JSON-RPC structural payload format required for a Google Developer API validation request?"
    )