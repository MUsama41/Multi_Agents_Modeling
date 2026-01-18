from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from ..config import settings

class InterpersonalAgent:
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=settings.groq_api_key, model_name=settings.model_name)

    async def process(self, idea: str):
        prompt = ChatPromptTemplate.from_template("""
            Persona: Warm, supportive, motivational partner.
            Encourage creativity and offer gentle guidance.
            Instructions:
            - If unclear: "Thanks for sharing! Could you tell me more?"
            - If simple: "Great start! Adding more details could make it stronger."
            - Max 4 lines. Warm tone.
            
            Idea: {idea}
        """)
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"idea": idea})
        
        return {"response": response.content.strip()}
