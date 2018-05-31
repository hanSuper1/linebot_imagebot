from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
import requests
from bs4 import BeautifulSoup
import json
import random

app = Flask(__name__)
mylist = []
# Channel Access Token
line_bot_api = LineBotApi('Il2mfzCoRy00MYBMc19GA6tW2RH4AqfxtdtGo2qLIAZ057J8DyyYE5NYaeEMapr11WBG1aNe2pomzJTxLRwqie1jt2EIM8Zuptxi95xHAFrMmsNVV+tL/DNHbfbb0ovkwLVzwU7fRe220wfmwGH5/QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('264fb5758b474343d5f90dcd110a877b')

url = 'https://www.google.com.tw/search?hl=zh-TW&authuser=0&tbm=isch&source=hp&biw=1365&bih=949&ei=GenRWqzqGYGq0gTvn7TIDQ&q='
header = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
currentText = ""
bonusList = []

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

imgs = []
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	mylist.append(event.message.text)
	if event.message.text == '00':
		message = TextSendMessage(text = 'text')
		line_bot_api.reply_message(event.reply_token, message)
	else:
			imgs = []
			keywords = event.message.text
			r = requests.get(url+keywords, headers = header)
			soup = BeautifulSoup(r.text, 'html.parser')
			
			results = soup.find_all('div', {'class' : 'rg_meta notranslate'})
			for result in results:
				result = result.get_text()
				jstr = result.replace("'", "\"")
				d = json.loads(jstr)
				#print(d['ou'])
				str = d['ou']
				if(str.find('https:') != -1):
					imgs.append(d['ou'])
					
			imageUrl = imgs[random.randint(0, len(imgs)-1)]
			message = ImageSendMessage(
				original_content_url=imageUrl,
				preview_image_url=imageUrl
			)
			if len(bonusList) == 0:
				bonusList.append('s')
				line_bot_api.reply_message(event.reply_token, message)
			else:
				message = ImageSendMessage(
					original_content_url='https://i.ytimg.com/vi/4kOX-qE6Ka4/maxresdefault.jpg',
					preview_image_url='https://i.ytimg.com/vi/4kOX-qE6Ka4/maxresdefault.jpg'
				)
				line_bot_api.reply_message(event.reply_token, message)
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
