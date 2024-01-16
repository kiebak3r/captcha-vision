import base64
import os
import shutil
import requests
import configparser
import datetime
import pyautogui as p


class GPT:
    def __init__(self):
        self.api = config.get('openai', 'api_key')
        self.prompt = config.get('openai', 'prompt', raw=True)
        self.max_tokens = int(config.get('openai', 'max_tokens'))
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api}"
        }

    def query(self):
        try:
            img = self.screenshot()
            base64_image = self.encode_image(img)
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": self.max_tokens
            }
            return payload
        except FileNotFoundError:
            print("Image not found, Check Path is correct in config.ini")
            quit(1)

    @staticmethod
    def encode_image(img):
        with open(img, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def screenshot():
        screenshot = p.screenshot()
        timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M")
        filename = f"img/screenshot_{timestamp}.jpg"
        screenshot.save(filename)
        return filename


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    if not os.path.exists("img"):
        os.mkdir("img")

    gpt = GPT()
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=gpt.headers,
        json=gpt.query()
    ).json()

    print(response["choices"][0]["message"]["content"])
    shutil.rmtree("img")
