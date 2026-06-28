from datetime import date
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


# 1. Define the strict JSON structure using Pydantic
class ExpenseReceipt(BaseModel):
    amount: float = Field(
        description="The total monetary value spent on the receipt."
    )
    category: str = Field(
        description="The type of expense (e.g., Travel, Food, Software, Equipment)."
    )
    merchant: str = Field(description="The name of the vendor or store.")
    transaction_date: date = Field(
        description="The date of the transaction in YYYY-MM-DD format."
    )  # Renamed from 'date' to 'transaction_date'


# 2. Initialize the Gemini Client
client = genai.Client()

# Messy input example
messy_user_input = (
    "Hey team, yesterday on June 18th I dropped $42.50 at Starbucks "
    "getting coffee and snacks for the client sync presentation. Put it under meals."
)

# 3. Call the model forcing a strict structured schema constraint
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messy_user_input,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ExpenseReceipt,
        temperature=0.0,
    ),
)

# Print the cleanly parsed, validated JSON output
print(response.text)