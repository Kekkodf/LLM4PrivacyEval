import os
import pandas as pd
from typing import List
import random
import instructor
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import time

class Character(BaseModel):
    #original_text: str = Field(..., description="The original text")
    #obfuscated_texts: list[str] = Field(..., description="The list of obfuscated texts")
    scores: list[float] = Field(..., description="The information leakage scores")
    justifications: list[str] = Field(..., description="Justifications for the scores")

#read the API key from a file, the key.txt file should be in the config folder, if not the script do not work
def read_key(file_name: str = "key.txt") -> List[str]:
    """
    Read the API key from a file
    """
    try:
        with open(f'./config/{file_name}') as file:
            apy_key_list = file.read().splitlines()
    except:
        print("The file with the API key was not found")
        os._exit(1)
    return apy_key_list

def read_data(path:str,
              **kwargs) -> List[pd.DataFrame]:
    """
    Read data from data folder
    """
    
    try:
        files = os.listdir(f'{os.getcwd()}/data/{path}')

    except:
        print("The folder with the data was not found")
        os._exit(1)
    dfs = []
    #order the files by the params
    files = sorted(files, key=lambda x: float(x.split("_")[-1].replace(".csv", "")))
    for file in files:
        if file.endswith(".csv"):
            df = pd.read_csv(f'./data/{path}/{file}')
            dfs.append(df)
    return dfs

def get_answers(df: pd.DataFrame, key_list: list[str], model: str = 'llama-3.3-70b-versatile') -> pd.DataFrame:
    """
    Get the information leakage scores and justifications for a set of obfuscated text variants
    with respect to their original text in batch mode.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing 'id', 'text', and 'obfuscatedText' columns.
        key_list (list[str]): List of API keys for the Groq client.
        model (str): The model name to use.

    Returns:
        pd.DataFrame: DataFrame containing scores and justifications for each obfuscated text.
    """
    final = pd.DataFrame(columns=['id', 'text', 'obfuscatedText', 'score', 'justification', 'model'])
    key = random.choice(key_list)
    client = Groq(api_key=key)
    client = instructor.from_groq(client, model=instructor.Mode.TOOLS)
    
    grouped = df.groupby('text')
    
    for original_text, group in grouped:
        obfuscated_texts = group['obfuscatedText'].tolist()
        ids = group['id'].tolist()
        
        context = [{
            "role": "system",
            "content": f"""
            Evaluate the information leakage from the original text to the obfuscated texts, providing a justification for each score given. 
            Consider lexical and semantic similarities between original and obfuscated texts.
            The score should be a float between 0 and 1, where 0 indicates no information leakage and 1 indicates complete information leakage.
            The original text is: {original_text}
            The obfuscated texts are: {obfuscated_texts}.
            Respond only with the scores and justifications for each obfuscated text as instructed.
            """
            #"content": f"""
            #    Evaluate the information leakage from the original text to the obfuscated texts, providing a justification for each score given. 
            #    The score should be a int between 1 and 5, where 1 indicates no information leakage and 5 indicates complete information leakage.
            #    Consider lexical and semantic similarities between original and obfuscated texts.
            #    The original text is: {original_text}. 
            #    The obfuscated texts are: {obfuscated_texts}.
            #    Respond only with the scores and justifications for each obfuscated text as instructed.
            #    """
        },
        {
            "role": "user",
                "content": f"Reply as instructed."
        }]
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=context,
                response_model=Character,
                max_tokens=500,
                temperature=0
            )
        except Exception as e:
            print(e)
            time.sleep(60)
            continue
        
        for id_, obf_text, score, justification in zip(ids, obfuscated_texts, response.scores, response.justifications):
            temp = pd.DataFrame([[id_, original_text, obf_text, score, justification, model]],
                                columns=['id', 'text', 'obfuscatedText', 'score', 'justification', 'model'])
            final = pd.concat([final, temp], ignore_index=True)
    return final
        
def retry(model, prompt, key):
    client = Groq(api_key=key)
    client = instructor.from_groq(client, model=instructor.Mode.TOOLS)
    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        response_model=Character,
        max_tokens=500,
        temperature=1.0
    )
    return response

def get_answers_deepseek(df: pd.DataFrame, key_list: list[str], model: str = 'deepseek-r1-distill-llama-70b') -> pd.DataFrame:
    """
    Get the information leakage scores and justifications for a set of obfuscated text variants
    with respect to their original text in batch mode.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing 'id', 'text', and 'obfuscatedText' columns.
        key_list (list[str]): List of API keys for the Groq client.
        model (str): The model name to use.

    Returns:
        pd.DataFrame: DataFrame containing scores and justifications for each obfuscated text.
    """
    final = pd.DataFrame(columns=['id', 'text', 'obfuscatedText', 'score', 'justification', 'model'])
    key = random.choice(key_list)
    
    grouped = df.groupby('text')

    for original_text, group in grouped:
        obfuscated_texts = group['obfuscatedText'].tolist()
        ids = group['id'].tolist()
        
        try:
            client = Groq(api_key=key)
            client = instructor.from_groq(client, model=instructor.Mode.TOOLS)
            response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                "role": "system",
                #"content": f"""
                #Evaluate the information leakage from the original text to the obfuscated texts, providing a justification for each score given. 
                #Consider lexical and semantic similarities between original and obfuscated texts.
                #The score should be a float between 0 and 1, where 0 indicates no information leakage and 1 indicates complete information leakage.
                #The original text is: {original_text}. 
                #The obfuscated texts are: {obfuscated_texts}.
                #Respond only with the scores and justifications for each obfuscated text as instructed.
                #"""
                "content": f"""
                Evaluate the information leakage from the original text to the obfuscated texts, providing a justification for each score given. 
                Consider lexical and semantic similarities between original and obfuscated texts.
                The score should be a int between 1 and 5, where 1 indicates no information leakage and 5 indicates complete information leakage.
                The original text is: {original_text}. 
                The obfuscated texts are: {obfuscated_texts}.
                Respond only with the scores and justifications for each obfuscated text as instructed.
                """
            },
            {
                "role": "user",
                "content": f"Reply as instructed."
            }
            ],
            temperature=1.0,
            #max_completion_tokens=500,
            stream=False,
            reasoning_format="hidden",
            response_model=Character,
        )
        except Exception as e:
            print(e)
            #time.sleep(60)
            continue
        
        for id_, obf_text, score, justification in zip(ids, obfuscated_texts, response.scores, response.justifications):
            temp = pd.DataFrame([[id_, original_text, obf_text, score, justification, model]],
                                columns=['id', 'text', 'obfuscatedText', 'score', 'justification', 'model'])
            final = pd.concat([final, temp], ignore_index=True)
    return final
