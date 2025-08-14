from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os
from crawl4ai import BrowserConfig, LLMConfig, CacheMode,  CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from scraper_format import ScraperFormat
from llmsetup import readenv


def deepcrawl_strategy():
    """
    Returns the deep crawling strategy for the crawler.
    
    Returns:
        BFSDeepCrawlStrategy: The strategy for deep crawling the web pages.
    """
    return BFSDeepCrawlStrategy(
        max_depth=1,
        include_external= False,
        
    )
def get_browser_config():
    """
    Returns the browser configuration for the crawler.
    
    Returns:
        BrowserConfig: Configuration object for the browser."""
    return BrowserConfig(
        browser_type="chromium",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        headless=False,
        viewport_width= 1280,
        viewport_height = 720,
        use_persistent_context= True,
        user_data_dir= r"C:\Users\PC\Desktop\program\LMcrawler\browsercookies",
        verbose=True,
    )

def get_llm_strategy()-> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.
    
    Returns:
        LLMExtractionStrategy: The setting for how to extract data using LLM"""
    return LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="ollama/llama3.2",
            api_token=readenv()[2],
            
        ),
        schema=ScraperFormat.model_json_schema(),
        extraction_type="schema",
        instructions=(
            "Extract all news with 'Websource', 'News Topic', 'URL', 'News summary', 'period' from the given HTML content."
            "the websource is the source of the news, the news topic is the main topic of the news,"
            "URl is the link to the news"
            "News summary is a brief summary of the news article from the URL."
            "period is the time when the news was published, it should be in the format of [dattetime, dayperiod]"
        ),
        input_format="markdown",
        verbose=True,
    )
def get_llm_strategy2()-> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.
    
    Returns:
        LLMExtractionStrategy: The setting for how to extract data using LLM"""
    return LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="ollama/llama3.2",
            api_token=readenv()[2],
            
        ),
        instructions=(
           "Extract all meaningful text content from paragraphs and inline spans that appear within article or div containers."

           "Summarize in a concise manner, focusing on the main points and key information"
        ),
        verbose=True,
    )

def get_crawler_config()-> CrawlerRunConfig:
    """
    Returns the configuration of the crawler.
    
    Returns:
        CrawlerRunConfig: The configuration for the crawler run.
    """
    selected_css = "c-wiz[class='D9SJMe']"
    return CrawlerRunConfig(
        extraction_strategy=get_llm_strategy(),
        #deep_crawl_strategy=deepcrawl_strategy(),
        cache_mode= CacheMode.BYPASS,
        css_selector= selected_css,
        page_timeout= 100000,   
        verbose=True,
        
    )
def get_deepcrawl_config()-> CrawlerRunConfig:
    """
    Returns the configuration for deep crawling.
    
    Returns:
        CrawlerRunConfig: The configuration for deep crawling.
    """
    return CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=get_llm_strategy2(),
        css_selector="div p, div span",
        page_timeout=100000,
        wait_for="div p, div span",
        simulate_user=True,
        verbose=True,
    )
