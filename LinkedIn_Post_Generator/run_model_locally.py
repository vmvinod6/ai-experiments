import requests

url = "http://localhost:12434/engines/llama.cpp/v1/chat/completions"

data = {
    "model": "ai/llama3.2:latest",
    "messages": [
        {
            "role": "system",
            "content": "you are helpful assistant."
        },
        {
            "role": "user",
            "content": "I wannt to buy a car, can you give me some suggestions?"
        }
    ],
    
    }
response = requests.post(url, json=data)
print(response.json())