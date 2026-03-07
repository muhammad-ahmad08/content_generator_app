import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_builder import build_prompt

# load environment variables
load_dotenv()

# initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_content(topic, tone):

    prompt = build_prompt(topic, tone)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content