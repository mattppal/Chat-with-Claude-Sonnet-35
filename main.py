import os

import gradio as gr
import anthropic

client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

MODEL = "claude-3-5-sonnet-20240620"


def chat_with_replit(message, history):

  messages = []
  response_content = ""

  for h in history:
    u = str(h[0])
    s = str(h[1])

    messages.append({"role": 'user', "content": u})
    messages.append({"role": 'assistant', "content": s})

  messages = messages + [
      {
          "role": "user",
          "content": str(message),
      },
  ]

  with client.messages.stream(
      max_tokens=1024,
      messages=messages,
      model=MODEL,
  ) as stream:
    for text in stream.text_stream:
      response_content += text

      yield response_content


js = """<script src="https://replit.com/public/js/replit-badge-v2.js" theme="dark" position="bottom-right"></script>"""

with gr.Blocks(fill_height=True, head=js) as demo:
  gr.ChatInterface(chat_with_replit,
                   fill_height=True,
                   examples=[
                       "What is the meaning of life?",
                       "What are some fun things to do in San Francisco?",
                       "Interpret 'The Road Not Taken' by Robert Frost"
                   ],
                   title="🚀 Chat with Claude Sonnet 3.5")

demo.launch(favicon_path="assets/favicon.png", allowed_paths=["assets"])
