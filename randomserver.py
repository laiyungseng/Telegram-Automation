import llmsetup
llmsetup.initenv()
llmsetup.readenv()
from mcp.server.fastmcp import FastMCP
import random
from praisonaiagents import Agent, Agents

mcp = FastMCP(name="Randomserver", host="127.0.0.1", port=5000)
@mcp.tool()
def randomreply(num1:int, num2:int)->int:
    """return random number"""
    a = random.randint(num1,num2)
    return f"this is your lucky number {a}"
@mcp.tool()
def greet(name:str)-> str:
    """Greet a user by name"""
    return f"Hello, {name}"

agent= Agent(
    role="tool specialize",
    llm="ollama/llama3.2",
    tools=[randomreply, greet]
)

if __name__ == "__main__":
    #mcp.run(transport="streamable-http")
    agent.launch(host="127.0.0.1", port=5000, protocol="mcp")

    
  