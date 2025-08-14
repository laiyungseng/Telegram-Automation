from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
from tqdm import tqdm
import random,time

##initializing default settings
search_enable = False
defaulturl="https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKTldTZ0FQAQ?hl=en-MY&gl=MY&ceid=MY%3Aen"
newinfo=[]
##setting up webdriver
user_agent =( "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36")
chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")
#chrome_options.add_argument("--headless") #silent scraping

def websurfing(defaulturl:str):
    driver = webdriver.Chrome(options=chrome_options)
    print("Getting Google News main page...")
    driver.get(defaulturl)
    mainhtml = driver.page_source
    mainsoup=BeautifulSoup(mainhtml, 'html.parser')     
    sleep(2)
    driver.close()
    return mainsoup

def randommousehouve(elements):
    """
    This function is random action that during browsing
    
    Searching for every <h1> tag in the html and randomly select one of the <h1> tag element. 
    """
    if not elements:
        return
    element = random.choice(elements)
    actions =ActionChains(driver)
    actions.move_to_element(element).perform()

def get_url(url:str)->str:
    """ Function to get the current URL.
    Returns:
        html: The HTML content of the Google News main page.   
    """
    ##search for the related information and parce all the html contain.
    driver = webdriver.Chrome(options=chrome_options)
    print("Getting current URL...") 
    current_url = driver.get(url)
    h1_tag = driver.find_element(By.CSS_SELECTOR, "h1")
    if h1_tag:
        randommousehouve(h1_tag)
    driver.execute_script("window.scrollBy(0, argument[0])", random.randint(200,800))
    time.sleep(random(0.5,2))
    new_url = driver.current_url
    print(new_url)
 
    return new_url

def search_function(inserttopic: str) -> bool:
    """
    Function to perform search for a specific topic on Google News.
    
    This function locates the search input field, enters the specified topic,
    and clicks the search button to initiate the search.

    Args:
        inserttopic (str): The topic to search for.
    Returns:
        bool: True if the search was suuccesful, False otherwise.
    """
    driver = webdriver.Chrome(options=chrome_options)
    global search_enable
    try:
        ##perform search on the topic
        search_input=driver.find_element(By.XPATH, '//input[@aria-label="Search for topics, locations & sources"]')
        search_input.send_keys(inserttopic)
        search_button=driver.find_element(By.XPATH, '//button[@role="button"]')
        ActionChains(driver)\
            .click(search_button)\
            .perform()
        search_enable = True
    except Exception as e:
        print(f"An error occurred: {e}")
        search_enable = False
    return search_enable

def filter_selection(htmlcontent:str):
    """
    This function perform filtering on the scraped news.
    
    the scraped infomation will be breakdown into format below:

    Return:
        List: Return the news in list format.
        info={
                'Headlines':{
                    'websource':[['the sources that produce the news'],...],
                    'topic':[['Title of the news'],...],
                    'url': [['URL of the news'],...],
                    'period: [['datetime','dayperiod'],...]
                    }
            }
    """
    infos =[]
    ##parcing
    ##if search_enable
    if not search_enable:
        ##search website title <h1>
        source_title=htmlcontent.find('h1', class_='BPNpve').text
        #print(source_title)
        ##saerch for news container
        search_source=htmlcontent.find_all('c-wiz', class_='PO9Zff Ccj79 kUVvS')
        #print(s.prettify())
        for i in search_source:
            sp = BeautifulSoup(str(i), 'html.parser')
            
            if sp.find(class_='LU3Rqb') or sp.find(class_='m5k28'):
                # infosource
                infosources = sp.find_all('div', class_="vr1PYe") 
                #print(infosource_txt)
                # all topic in google news
                topics = sp.find_all('a', class_="gPFEn") or sp.find_all('a',  class_="JtKRv")
                #print(topic_txt)
                # URL in google news
                urls_txt = ["https://news.google.com/"+(tag['href']).strip('./') for tag in sp.find_all('a', class_="gPFEn")]
                #print(urls_txt)
                # period in google news for the article
                periods = sp.find_all('time')
                datetime = sp.find('time')['datetime']
                period_txt= [(datetime,period.text) for period in periods]
                #print(period_txt)
                infos.append({
                    f'{source_title}':{
                    'websource': [infosource.text for infosource in infosources],
                    'topic': [topic.text for topic in topics],
                    'url': urls_txt,
                    'period': period_txt,
                    }
                })

        return infos
    else:
        search_source = get_url().find_all('article', class_="IFHyqb DeXSAc")
    
        for i in range(len(search_source)):
            sp_source = BeautifulSoup(f'{search_source[i]}','html.parser')
            infosource = sp_source.find('div', class_='vr1PYe').text
            topic=sp_source.find('a', class_='JtKRv').text
            url ="https://news.google.com"+ sp_source.find('a',class_='JtKRv')['href']
            datetime= sp_source.find('time')['datetime']
            dayperiod = sp_source.find('time').text
            info =   {
            "AMD news":[{
                "websources":infosource,
                "News Topic":topic,
                "URL": url,
                "period": [datetime, dayperiod],
            }]
            },
            infos.append(info)
    #verify data
    #print(infos[0])
    #print(len(infos))
    #print(infos[1][0])
     
def split_headlines_by_index(data:list)->str:
    """
    This function is to filter the combined list into separate list.

    it will breakdown the single list element into multiple list element according to its index

    Return:
        List: split into single list element instead of multiple element in a single list.
        Example={
                    "Topic": "title of the object",
                    "url": "url of the object",
                    "period":["datetime", "display"]
                    }
    """
    split_data = []
    for i in range(len(data)):   
        headlines = data[i].get('Headlines', {})
        websources = headlines.get('websource', [])
        topics = headlines.get('topic', [])
        urls = headlines.get('url', [])
        periods = headlines.get('period', [])

        # Safeguard: use min length to avoid IndexError
        entry_count = min(len(websources), len(topics), len(urls), len(periods))

        for i in range(entry_count):
            entry = {
                'headline': {
                    'websource': websources[i],
                    'topic': topics[i],
                    'url': urls[i],
                    'period': {
                        'datetime': periods[i][0],
                        'display': periods[i][1]
                    }
                }
            }
            split_data.append(entry)  
    return split_data

def timeparser(example:str):
    """
    This function is to convert display time the extract from the information.
    
    The time format is listed below:
    'display': ['1 days ago', '1 hours ago', '1 minutes ago, '1 weeks ago']

    either one of the unit found in the display will be filter according to days, hours, minutes and weeks.
    Return:
        timedelta(hours=float(num)): hours depend on the units from the display and num is the number of the units.
    """
    time_str = example
    parts = time_str.split()
    if 'ago' in parts: #check is ago in the content information
        num = str(parts[0])
        unit = parts[1]
    elif 'Yesterday' in parts:
        return timedelta(days=1)
    elif len(parts) == 2 and parts[0].isdigit() and parts[1].isalpha():
        return timedelta(days=999)  # treat as non-recent

    try:
        if 'hours' in unit: #if hour found convert to timedelta:hours
            return timedelta(hours=float(num))
        elif 'days' in unit: #if days found convert to timedelta:days
            return timedelta(days=float(num))
        elif 'minutes' in unit: #if minutes found convert to timedelta:minutes
            return timedelta(minutes=float(num))
        elif 'weeks' in unit:
            return timedelta(weeks=float(num))
    except (ValueError, IndexError):

        print("no unit found")
        pass

def datetime_filter(infos:list, duration:float =6, unit: str="hour")-> list:
    """
    Filters entries in the infos list by display using timedelta logic.

    Args:
        infos (list): List of dictionaries with 'headline' → 'period' → 'display' fields.
        duration (float, optional): Duration threshold. Defaults to 6.
        unit (str, optional): Time unit for the threshold. Supported values:
            - 'minutes'
            - 'hours'
            - 'days'
            - 'weeks'
          Defaults to 'hour'.

    Returns:
        list: Filtered entries newer than the specified duration.

    Example:
        datetime_filter(news_items, duration=12, unit="hours")
        → Returns entries published in the last 12 hours.
    """
    filtered_info=[]
    #filter the duration based on the user input
    try:
        unit.lower()
        if unit == "hours":
            cutoff = timedelta(hours=duration)
        elif unit == "minutes":
            cutoff = timedelta(minutes=duration)
        elif unit == "days":
            cutoff= timedelta(days=duration)
        elif unit == "Weeks":
            cutoff = timedelta(weeks=duration)
    except Exception as e:
        print(f"Error building cutoff: {e}")
        return
    #filter information based on the date
    for info in range(len(infos)):
        h = infos[info].get('headline')
        duration = h.get('period',{}).get('display')
        date_str = timeparser(duration)
        if date_str:
            if date_str <=  timedelta(unit = duration):
                filtered_info.append(infos[info])  
    return filtered_info

def checklogfile():
    """
    This function is to check the does the require file 'latestnews.json' and 'pendingupload.json' exist in the file directory
    
    If no specific file found, create a new file.
    
    Else print both file exist as a alert to user.
    
    """
    jsonfilepath = r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson"
   
    print("Scanning library folder....")
    #print(os.listdir(jsonfilepath))
    if os.path.exists(os.path.join(jsonfilepath, "latestnews.json")) and os.path.exists(os.path.join(jsonfilepath, "pendingupload.json")):
        print(f"Both files exist in {jsonfilepath}.")
        print("Skipping file creation process.")
    else:
        try:
            if "latestnews.json" not in os.listdir(jsonfilepath) :
                print(f"file latestnews.json not found in the {jsonfilepath}!!")
                print("initializing...file")
                open(os.path.join(jsonfilepath,"latestnews.json"), "x")
                print(f"File created in {jsonfilepath}.")
            elif "pendingupload.json" not in os.listdir(jsonfilepath):
                print(f"file pendingupload.json not found in the {jsonfilepath}!!")
                print("initializing...file")
                open(os.path.join(jsonfilepath, "pendingupload.json"), "x")
                print(f"File created in {jsonfilepath}.") 
        except Exception as e:
            print(f"Error found in checking jsonfile in {jsonfilepath}, error:{e}")
    return

def savefiles(infos:list):
    """
    This function is to save the content from the past 1 days news that had been uploaded to the destination
    
    This function also a records of past data that had been sent to the destination
    """
    with open(r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson\latestnews.json", 'a', encoding='utf-8') as fl:
        json.dump(infos, fl, indent=2, ensure_ascii=False)
        fl.write("/n")

def checkcontent(infos:list):
    """
    This function is to check is there new news from the available, if got will pass to pending upload json file.
    """
    new_contents = []
    try:
        with open(r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson\latestnews.json", "r") as fl:
            existing_file = json.load(fl)
    except json.JSONDecodeError:
        existing_file=[{}]
   
    for info in range(len(infos[0])):
        cont = infos[0][info].get('headline', [])
        topic = cont.get('topic',{})
        try:
            existing_topic = [existing_news['headline']['topic'] for existing_news in existing_file[0]] 
        except (KeyError, IndexError, TypeError):
            existing_topic=[]
        if topic not in existing_topic:
                new_contents.append(cont)
    if new_contents:   
        with open(r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson\pendingupload.json", "a", encoding='utf-8') as fu:
            json.dump(new_contents, fu, indent=2, ensure_ascii=False)
            fu.write("\n")
        print(f"Total of {len(new_contents)} new news had been saved in pendingupload.json.")
    else:
        print("No new news update, Nothing added")

def replaceurl(infos:str):
    driver = webdriver.Chrome(options=chrome_options)
    for idx, info in enumerate(tqdm(range(len(infos[0])), desc="Replacing URL")):
       url = infos[0][info].get('headline').get('url')
       newurl = get_url(url)
       newinfo[0][info]['headline']['url']=newurl
       if (idx+1)%10==0:
            driver.quit()
    return infos
      
def scrapemain():
    all_news_content = split_headlines_by_index(filter_selection(websurfing(defaulturl)))
    newinfo.append(datetime_filter(all_news_content))
    #replaceurl(newinfo)
    checkcontent(newinfo)
    print("Done upload the latest news to pendingupload.")
    
def logfilterclean(duration:float=6, unit: str="hours")->str:
    """
    This function is to scan the latestnews log to remove if the information is more than duration.
    
    Args:
        duration (float, optional): Duration threshold. Defaults to 6.
        unit (str, optional): Time unit for the threshold. Supported values:
            - 'minutes'
            - 'hours'
            - 'days'
            - 'weeks'
          Defaults to 'hour'.

    Returns:
        list: Filtered entries newer than the specified duration.

    Example:
       logfilter(duration=12, unit="hours")
        → Returns entries published in the last 12 hours.
    """
    cleanedtime=[]
    uploadfile = r"C:\Users\PC\Desktop\program\LMcrawler\latestnewssavejson\latestnews.json"
    with open(uploadfile,'r', encoding='utf-8') as f:
        contents = json.load(f)
    try:
        unit.lower()
        if unit == "hours":
            cutoff = timedelta(hours=duration)
        elif unit == "minutes":
            cutoff = timedelta(minutes=duration)
        elif unit == "days":
            cutoff= timedelta(days=duration)
        elif unit == "Weeks":
            cutoff = timedelta(weeks=duration)
    except Exception as e:
        print(f"Error building cutoff: {e}")
        return
    for content in contents:    
        duration = content['period']['display']
        contduration = timeparser(duration)
        if contduration < cutoff:
            cleanedtime.append(content)
    with open(uploadfile, 'w', encoding='utf-8') as cleanfile:
        json.dump(cleanedtime, cleanfile, indent=2, ensure_ascii=False)


# if __name__=="__main__":
#     checklogfile()
#     scrapemain()