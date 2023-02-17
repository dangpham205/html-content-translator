import os
from googletrans import Translator
from bs4 import BeautifulSoup
from decouple import config

    
def translate_worker(html_files, start,end):

    html_files = sorted(html_files, key=lambda x: os.path.getsize(x))

    half_length = len(html_files) // 2
    result = []
    for i in range(half_length):
        result.append(html_files[i])
        result.append(html_files[-(i+1)])
    if len(html_files) % 2 != 0:
        result.append(html_files[half_length])
    

    for html_file in result[start:end]:

        with open("translating_files.txt", "a") as file:
            file.write(f"{html_file}\n")
        print(f'Processing file: {html_file} || {start+1}/{len(html_files)}')

        # Open the HTML file and read its contents
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')  

        try:
            translator = Translator()
            target_language = config('dest_language')
            no_translate_tags = ['script', 'style', 'head', 'meta', 'link']
            # delete all <iframe> tags
            for iframe in soup.find_all('iframe'):
                iframe.decompose()

            # translate the texts in the body tag and replace them in the original html contents
            for tag in soup.body.descendants:
                # Check if the tag has text content and is not inside a script or style tag
                if hasattr(tag, 'string') and tag.parent.name not in no_translate_tags and tag.name not in no_translate_tags:
                    translated_text = translator.translate(tag.string, dest=target_language).text
                    if tag.string and translated_text:
                        tag.string = translated_text

            
            with open(html_file, "w", encoding="utf-8") as file:
                file.write(str(soup))
                
            with open("translated_files.txt", "a") as file:
                file.write(f"{html_file}\n")
        except Exception as e:
            with open("failed_files.txt", "a") as file:
                file.write(f"{html_file}\n")
            print(html_file,e)
            continue
