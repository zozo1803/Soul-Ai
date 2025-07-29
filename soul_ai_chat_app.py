import streamlit as st
import os
import openai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Mocked SOUL classes/functions for deployment
class SoulAITradingSystem:
    def __init__(self):
        self.soul = self
        self.memory = {}

    def _analyze_stock(self, symbol):
        return {"recommendation": {"action": "BUY", "confidence": 0.87}}

    def _execute_paper_trade(self, symbol, direction, amount):
        return {"symbol": symbol, "direction": direction, "price": 2500, "shares": amount / 2500}

def interpret_command(text, soul_ai):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are SOUL AI, a stock trading assistant."},
                {"role": "user", "content": text}
            ]
        )
        intent = response.choices[0].message.content.strip().lower()

        if intent.startswith("analyze"):
            parts = intent.split()
            if len(parts) < 2:
                return "❓ Please provide a symbol to analyze."
            symbol = parts[1]
            analysis = soul_ai._analyze_stock(symbol)
            return f"📊 Analysis for {symbol}:\nRecommendation: {analysis['recommendation']['action']} with confidence {analysis['recommendation']['confidence']*100:.1f}%."

        elif intent.startswith("paper_trade"):
            parts = intent.split()
            if len(parts) < 4:
                return "❓ Usage: paper_trade <symbol> <direction> <amount>"
            symbol, direction, amount = parts[1], parts[2].upper(), float(parts[3])
            result = soul_ai._execute_paper_trade(symbol, direction, amount)
            return f"🧾 Paper trade executed: {result['shares']:.2f} shares of {symbol} at ₹{result['price']:.2f} [{direction}]"

        else:
            return "❌ I didn't understand that command."

    except Exception as e:
        return f"💥 Error: {e}"

# Streamlit App
st.set_page_config(page_title="SOUL AI Chat App", page_icon="🧠")
st.title("🧠 SOUL AI - Stock Market Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask SOUL something...")
ai = SoulAITradingSystem()

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    reply = interpret_command(user_input, ai)
    st.session_state.chat_history.append(("SOUL", reply))

for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧍 {speaker}:** {msg}", unsafe_allow_html=True)
    else:
        st.markdown(f"**🤖 {speaker}:** {msg}", unsafe_allow_html=True)