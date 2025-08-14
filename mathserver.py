# server.py
from mcp.server.fastmcp import FastMCP
import math

# Create an MCP server
mcp = FastMCP(name="Math",host="127.0.0.1", port=8080, timeout=30)

@mcp.tool()
def add(a:str, b:str) -> str:
    """add two numbers"""
    return a + b

@mcp.tool()
def multiple(a:int, b:int) -> int:
    """multiply two numbers"""
    return a * b

# Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"

#The transport="stdio" argument tells the server to:
# Use standard input/output (stdin and stdout) to receive and respond to tool function calls 

if __name__ == "__main__":
    print("initiating the mathserver....")
    mcp.run()