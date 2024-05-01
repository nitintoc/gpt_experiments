import os
import openai
import requests
import bs4

def create_prompt(headlines):
  """
  A function used to create the required prompt for the LLM
  """
    joined = "\n".join(headlines)
    prompt = f"Translate the following into English:\n{joined}"
    return prompt


#Add the API key here
os.environ["API_KEY"] = ""
openai.api_key = os.getenv("API_KEY")

response = requests.get('https://ricette.giallozafferano.it/Torta-tenerina.html')
if response:
  print("Website works..")

soup = bs4.BeautifulSoup(response.text, 'lxml')
headline = [h.getText() for h in soup.select('title')]
ingredients = [h.getText() for h in soup.select('dd.gz-ingredient a')]
recipie = headline + ingredients
prompting = create_prompt(recipie)

response = openai.completions.create(
    model = "gpt-3.5-turbo-instruct",
    prompt = prompting,
    temperature = 0.1,
    max_tokens = 200,
    )

translated = response.choices
for item in translated:
    print(item.text)
