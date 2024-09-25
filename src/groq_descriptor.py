
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the image:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://i.ibb.co/D5jn3pK/test5-real.jpg",
                    },
                },
            ],
        }
    ],
    model="llava-v1.5-7b-4096-preview",
)

print(chat_completion.choices[0].message.content)




# from openai import OpenAI
# from os import getenv

# # gets API Key from environment variable OPENROUTER_API_KEY
# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=getenv("OPENROUTER_API_KEY"),
# )

# import base64
# import httpx

# image_url = "https://ibb.co/pwFzz26"

# image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
# completion = client.chat.completions.create(
#   model="qwen/qwen-2-vl-7b-instruct:free",
#   messages=[
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "Who are you?"
#             },
#             {
#                 "type": "image_url",
#                 "image_url": {"url": image_url}
#             }
#         ]
#     }
#   ],
# )
# print(completion)



# import requests
# import json
# import base64


# # Load and encode image as base64
# image_url = "https://ibb.co/pwFzz26"
# image_data = requests.get(image_url).content
# encoded_image = base64.b64encode(image_data).decode('utf-8')


# api_key=getenv("OPENROUTER_API_KEY")

# # Create request
# response = requests.post(
#   url="https://openrouter.ai/api/v1/chat/completions",
#   headers={
#     "Authorization": f"Bearer {api_key}",
#   },
#   data=json.dumps({
#     "model": "mistralai/pixtral-12b:free",
#     "messages": [
#       {
#         "role": "user",
#         "content": "What is in this image?"
#       },
#       {
#         "role": "user",
#         "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}]  # Sending the image as base64
#       }
#     ],
#     "top_p": 1,
#     "temperature": 0.9,
#     "frequency_penalty": 0,
#     "presence_penalty": 0,
#     "repetition_penalty": 1,
#     "top_k": 0
#   })
# )

# print(response.json())














