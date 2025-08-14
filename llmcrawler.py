import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from scraper_format import ScraperFormat
import os
from scrapper_utils import get_browser_config, get_llm_strategy, get_crawler_config, get_deepcrawl_config



async def main():

    browser_config = get_browser_config()
    crawler_config = get_crawler_config()
    deepcrawl_config= get_deepcrawl_config()
    llm_config = get_llm_strategy()
    results_info=[]

    #Start the web crawler context
    # URL
    async with AsyncWebCrawler(config=browser_config) as crawler:
        init_results = await crawler.arun("https://news.google.com/search?q=AMD%20nes&hl=en-MY&gl=MY&ceid=MY%3Aen", config=crawler_config)
        links = init_results.links.get("internal", [])
        
        if init_results.success:
            print(f"Initial crawl successful:", init_results.extracted_content)

        for link in links[:5]:
            print(link)
            results = await crawler.arun(f"{link['href']}",
                                         config= deepcrawl_config)
    
            print("Result from external link:", results.extracted_content)
            for result in results.extracted_content:
                if result:
                    results_info.append(result)
                else:
                    print(f"No results found for {link['href']}")
        print("Crawling completed for all links.")
        print(results_info)
asyncio.run(main())
              