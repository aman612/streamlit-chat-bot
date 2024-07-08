import openai

openai.api_key = 'fake-api'
openai.base_url = "http://localhost:3040/v1/"

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "why Python is better than Js"},
    ],
)

print(completion)