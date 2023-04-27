import os
import logging
from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import quote
import openai

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_openai_generated_text(prompt):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
      "role": "system",
      "content": "You are a character from the show."
    }, {
      "role": "user",
      "content": prompt
    }],
    max_tokens=300,
    temperature=0.8)
  logging.debug(response)
  return response.choices[0].message.content


def send_discord_message(content):
  data = {'content': content}
  requests.post(DISCORD_WEBHOOK_URL, json=data)


@app.route('/webhook', methods=['POST'])
def webhook():
  logging.info(request.headers)
  logging.info(request.data)

  if not request.data:
    logging.warning('Empty request payload')
    return jsonify(success=False, message='Empty request payload'), 400

  try:
    data = json.loads(request.data)
  except json.JSONDecodeError:
    logging.warning('Invalid JSON payload')
    return jsonify(success=False, message='Invalid JSON payload'), 400

  data = request.json
  logging.debug(f"Received webhook data: {data}")

  username = data['user']
  episode_name = data['episode_name']
  show_name = data['show_name']
  season_num = data['season_num']
  episode_num = data['episode_num']
  prompt = f"{episode_name} of {show_name}. You are an important character from this episode. Express the general sentiment of this episode through recognizable dialogue. Only respond in first person dialogue from that character. Don't say who you are. Say something to get people excited for the next episode, include a small detail about it. Be very brief"
  generated_text = get_openai_generated_text(prompt)

  logging.debug(f"Generated text: {generated_text}")

  message = f"📺 {username} just watched season {season_num} episode {episode_num} of {show_name} - {episode_name} !\n\n{generated_text}"

  logging.debug(f"Message: {message}")
  send_discord_message(message)

  return jsonify(success=True)


if __name__ == '__main__':
  logging.info("Starting server...")
  app.run(host='0.0.0.0', port=5000)
  logging.info("Server Shutting Down...\n")
