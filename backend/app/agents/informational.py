from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient
from ..config import settings

class InformationalAgent:
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=settings.groq_api_key, model_name=settings.model_name)
        self.tavily = TavilyClient(api_key=settings.tavily_api_key)
        self.information_context = """
        # Helpfull information and statistics
        - 91% of remote teams report improved collaboration with scheduled weekly progress updates (Gartner, 2019).
        - 61% of teams achieve higher productivity when tasks are well-defined and prioritized (Harvard Business Review, 2019).
        - 76% of remote workers favor a single channel for project updates (Stanford University, 2018).
        """

    async def process(self, question: str):
        prompt = ChatPromptTemplate.from_template("""
            Generate a minor variation in the provided information for the user question. 
            Variation should be minimal to avoid bias. Return only bullet points.
            Format: - [Statistic] ([Source, Year]). Example: [Application]
            
            Question: {question}
            Information: {information}
        """)
        
        chain = prompt | self.llm
        ai_response = await chain.ainvoke({"question": question, "information": self.information_context})
        
        # Fetch references
        try:
            tavily_res = self.tavily.search(query=question, num_results=3)
            references = [{"title": r.get("title"), "url": r.get("url")} for r in tavily_res.get("results", [])]
        except:
            references = []

        # Evaluation logic (simplified from original)
        eval_prompt = ChatPromptTemplate.from_template("""
            Review the response for accuracy and clarity preserving original meaning.
            Response: {response}
        """)
        eval_chain = eval_prompt | self.llm
        evaluation = await eval_chain.ainvoke({"response": ai_response.content})

        return {
            "response": ai_response.content.strip(),
            "evaluation": evaluation.content.strip(),
            "references": references
        }
