import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from crawl4ai import AsyncWebCrawler


# async def example():
#     transport = StreamableHttpTransport("http://127.0.0.1:5000/mcp")
#     async with Client(transport=transport) as client:
#         await client.ping()
#         print("Ping successful!")
        
#         tools = await client.list_tools()
#         print("Available:", tools)

#         # greeting = await client.call_tool("greet", {"name":"Alice"})
#         # print("Greeting result:", greeting)

#         # randomint = await client.call_tool("randomreply")
#         # print("random number:",randomint)

#asyncio.run(example())

async def main():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://crawl4ai.com")

        # Print the extracted content
        print(result.markdown)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
