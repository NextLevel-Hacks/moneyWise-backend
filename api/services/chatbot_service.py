import google.generativeai as genai
from config.settings import settings
import re

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class ChatbotService:
    def __init__(self):
        # Initialize the Gemini model with system instructions
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Use a suitable model
            system_instruction=(
                "You are a financial assistant for CashFlow Compass, a platform that helps users manage their finances. "
                "You can answer questions about financial summaries (e.g., total amount, amount debited), spending habits (e.g., spender type, spending analysis), "
                "and investment recommendations (e.g., what to invest in). "
                "Use the provided user data to give accurate answers. "
                "If a question is outside the scope of finance or CashFlow Compass (e.g., weather, general knowledge), "
                "respond with: 'Sorry, I can only assist with financial questions related to CashFlow Compass. Please ask about your finances or investments!'"
            )
        )

    def clean_response(self, text: str) -> str:
        text = re.sub(r'\*\*', '', text)  
        text = re.sub(r'\*', '', text)    
        text = re.sub(r'#+', '', text)    
        text = re.sub(r'- ', '', text)    
        text = re.sub(r'\n+', '\n', text)  
        text = re.sub(r'\s+', ' ', text)   
        return text.strip()  

    def get_response(self, user_id: str, message: str, db) -> str:
        transaction_summary = db["transactions"].find_one({"user_id": user_id})
        insights = db["insights"].find_one({"user_id": user_id})

        # Build the context for the chatbot
        context = "User data:\n"
        if transaction_summary:
            context += (
                f"Total Amount: ${transaction_summary['total_amount']}\n"
                f"Amount Remaining: ${transaction_summary['amount_remaining']}\n"
                f"Amount Debited: ${transaction_summary['amount_debited']}\n"
                f"AI Investment: ${transaction_summary['ai_investment']}\n"
            )
        if insights:
            context += (
                f"Spender Type: {insights['spender_type']}\n"
                f"Summary: {insights['summary']}\n"
                f"Spending Analysis: {insights['spending_analysis']}\n"
            )

        # Combine context and user message
        prompt = f"{context}\nUser question: {message}"

        try:
            response = self.model.generate_content(prompt)
            cleaned_response = self.clean_response(response.text)
            return cleaned_response
        except Exception as e:
            return f"Error generating response: {str(e)}"

chatbot_service = ChatbotService()