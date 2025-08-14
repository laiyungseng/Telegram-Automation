import llmsetup
llmsetup.initenv()
llmsetup.readenv()
import threading
import asyncio
import os
import subprocess
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp import Client
from praisonaiagents import Agent, MCP, Task
import requests


async def initsvr():
    scriptlocation=r"C:\Users\PC\Desktop\program\LMcrawler\randomserver.py"
    print("initializing server....")
    #start server at background
    subprocess.Popen(["python", scriptlocation])
    print("Server established!")


async def main():
    # transport = StreamableHttpTransport("http://127.0.0.1:5000/mcp")
    # async with Client(transport=transport) as client:
    #     await client.ping()
    #     print("Connection established...!")
    #     print("check available tool...")
    #     tools = await client.list_tools()
    #     print(tools)

    testmcp = Agent(
        name="randomclient",
        instructions="Choose and Call the correct tool to solve the question.",
        role="you are a helpful assistance that can access to a tool.",
        llm = "ollama/llama3.2",
        tools= MCP("http://127.0.0.1:5000/sse")
        )
    testmcp.start("i want you to generate a random number between 1 to 20. use the randomreply tool.")

if __name__=='__main__':
    #asyncio.run(initsvr())
    asyncio.run(main())
   