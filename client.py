import llmsetup
print("initializing LLM environment....")
llmsetup.readenv()
llmsetup.initenv()
from praisonaiagents import Agent, MCP, PraisonAIAgents,Task
from langchain_ollama import ChatOllama
import asyncio


async def main():
    #agent workflow setup
    new_agent1 = Agent(
        name= "math calculation",
        instructions = "Your are helpful assistant with access to a tool. Call it when the user ask for it.",
        llm ="ollama/llama3.2",
        tools=MCP("python mathserver.py")
    ) 
    task1_1 = Task(
        name= "analysing",
        description="Understand the provided question and solve the question with your processed tools",
        expected_output = "provide the correct answer to the first question",
        agent=new_agent1
    )
    task1_2= Task(
        name="summarydetailprocess",
        description="describe your though of action to solve the question",
        expected_output="provide the list of action to how you solve the question include what tool you selected",
        agent=new_agent1
    )
    # ##new agent2##
    # new_agent2=Agent(name= "random reply",
    #     instructions = "Your are helpful assistant with acess to a tool. Call it when the user ask for it.",
    #     llm ="llama3.2",
    #     tools=MCP("http:127.0.0.1:8000/mcp"))
    
    # task2_1=Task(
    #     name="randomreply",
    #     description="reply according to the user question",
    #     expected_output="reply according to the user question",
    #     agent=new_agent2
    # )
    
    agents = PraisonAIAgents(
        agents=[new_agent1],
        tasks=[task1_1,task1_2],
        process="sequential",
        verbose =True
    )
  
    agents.start("What is (1+20)X40?")
#environment for llm conneciton setup



asyncio.run(main())