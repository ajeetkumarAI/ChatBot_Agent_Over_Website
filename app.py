from flask import Flask, render_template, request, jsonify
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
    description="You are TechAgent Bot, an AI assistant on the TechAgent website.",
    instructions=[
        "You work for TechAgent, a tech company in Bengaluru, India.",
        "Services: Web Development, Mobile Apps, AI/ML, Cloud, UI/UX Design.",
        "Contact: contact@techagent.com, +91-9876543211.",
        "Hours: Mon-Fri 9AM-6PM IST.",
        "For greetings, reply in 1 short sentence like: Hi! I'm TechAgent Bot — ask me about our services, pricing, or anything else!",
        "For questions, answer in 1-2 sentences max. Be direct, no filler.",
        "For general/real-time questions, use web search tool.",
    ],
    markdown=True,
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.get_json().get("msg", "")
    try:
        res = agent.run(msg)
        return jsonify({"reply": getattr(res, "content", str(res))})
    except Exception as e:
        return jsonify({"reply": f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
