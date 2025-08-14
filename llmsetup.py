import subprocess
import os
from dotenv import load_dotenv
import requests
import asyncio

def readenv():
    #read from environemnt file
    
    PATH_TO_MAIN_PROGRAM_FOLDER=r"C:\Users\PC\Desktop\program\LMcrawler"
    main_filepath=os.listdir(PATH_TO_MAIN_PROGRAM_FOLDER)
    if "env.env" in main_filepath:
        #load data from environment file
        load_dotenv(dotenv_path=os.path.join(PATH_TO_MAIN_PROGRAM_FOLDER,"env.env"))
        OPENAI_BASE_URL= os.getenv("OPENAI_BASE_URL")
        MODEL_NAME= os.getenv("MODEL_NAME")
        OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
    else: 
        print("no env.env found in the directory!!")
    return OPENAI_BASE_URL,MODEL_NAME, OPENAI_API_KEY


def initenv():
    url,model_name,api_key = readenv()
    url = ''.join(["$env:OPENAI_BASE_URL=", f"'{url}'"])
    model_name = "".join(["$env:MODEL_NAME=", f"'{model_name}'"])
    api_key = "".join(["$env:OPENAI_API_KEY=", f"'{api_key}'"])

    initurl = subprocess.run(["powershell","-command",url], capture_output=True, text=True)
    initmodel_name = subprocess.run(["powershell","-command",model_name], capture_output=True, text=True)
    initapi_key = subprocess.run(["powershell","-command",api_key], capture_output=True, text=True)
    
    if initurl.returncode and initmodel_name.returncode and initapi_key.returncode != 0:
        print("An error occured: %s", initurl.stderr)
        print("An error occured: %s", initmodel_name.stderr)
        print("An error occured: %s", initapi_key.stderr)
    else:
        print("LLM model Intialize successfully!!")

    return


if __name__=="__main__":
    try:
        print("Scanning environment files....")
        readenv()
        print("Done scanning the environment files")
        print("Initializing environment for configuration in env file....")
        initenv()
        print("Done initialize LLM configuration.")
    except Exception as e:
        print("Initialization error please check llmsetup.py")
  



