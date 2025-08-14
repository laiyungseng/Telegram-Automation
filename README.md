# Google News Scraper & Notifier

This project is designed to automate the process of scraping the latest news from Google News, cleaning and filtering the data, and sending timely updates to users via Telegram.

## Features

- **Web Scraping:** Utilizes [crawl4ai](https://pypi.org/project/crawl4ai/), [Selenium](https://www.selenium.dev/), and [BeautifulSoup (bs4)](https://www.crummy.com/software/BeautifulSoup/) to reliably extract news data from Google News.
- **Data Cleaning:** Automatically removes unnecessary strings, boilerplate text, and filters out outdated or irrelevant news articles.
- **Timely Notifications:** The most recent and relevant news articles are pushed directly to users through Telegram.

## Workflow

1. **Scraping:** The script navigates Google News using Selenium and extracts data using BeautifulSoup and crawl4ai.
2. **Cleaning & Filtering:** Raw data is processed to remove noise and old articles, ensuring only the latest and most relevant news is retained.
3. **Delivery:** Clean news summaries are sent to users via Telegram bot.

## Requirements

- Python 3.11+
- crawl4ai
- selenium
- beautifulsoup4 (bs4)
- requests
- python-telegram-bot

## Installation

```bash
pip install crawl4ai selenium beautifulsoup4 requests python-telegram-bot
```

Make sure you have the appropriate WebDriver (e.g., ChromeDriver) for Selenium installed and available in your PATH.

## Usage

1. **Set up your Telegram bot:**  
   Create a Telegram bot with [BotFather](https://core.telegram.org/bots#botfather) and get your bot token.

2. **Configure environment variables or config file:**  
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: The chat ID to send news to

3. **Run the script:**  
   ```bash
   python main.py
   ```

## Customization

- **Filtering Criteria:**  
  You can modify the cleaning/filtering logic to suit specific keywords, timeframes, or sources.
- **Notification Frequency:**  
  Update the scheduling logic to control how often news is scraped and sent.

## License

[MIT](LICENSE)

## Credits

- [crawl4ai](https://github.com/your/crawl4ai)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [python-telegram-bot](https://python-telegram-bot.org/)

