from pydantic import BaseModel

class ScraperFormat(BaseModel):
    """
    Represents the format data structure of news.
    """
    websources: str
    topic: str
    url: str
    summary: str  # Summary of the news article
    period: list[str] #list of datetime and dayperiod, e.g. ["2023-10-01T12:00:00Z", "1Day"]