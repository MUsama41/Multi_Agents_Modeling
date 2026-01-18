from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from ..config import settings

class DecisionMakingAgent:
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=settings.groq_api_key, model_name=settings.model_name)
        self.unclear_keywords = [
            "unclear", "unrealistic", "confusing", "does not make sense", "vague", "ambiguous"
        ]

    async def process(self, idea: str):
        prompt = ChatPromptTemplate.from_template("""
            Persona: Supportive and motivational idea evaluator.
            Instructions:
            - If unclear: "The idea doesn't make sense. Try again with a clearer concept!"
            - If simple: "Good starting point! Consider adding more details."
            - Max 4 lines.
            
            Idea: {idea}
        """)
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"idea": idea})
        content = response.content.strip()
        
        score = sum(1 for kw in self.unclear_keywords if kw in content.lower())
        
        return {
            "response": content,
            "idea_score": score
        }
