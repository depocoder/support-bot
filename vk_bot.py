import os
import random
import logging
import time
from tg_bot import detect_intent_texts
from requests.exceptions import ConnectionError
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def reply_from_dialogflow(event, vk_api):
    project_id = os.getenv("PROJECT_ID")
    language_code = os.getenv("LANGUAGE_CODE")
    response = detect_intent_texts(
        project_id, event.user_id, event.text, language_code)
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()
    while True:
        try:
            vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
            vk_api = vk_session.get_api()

            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    reply_from_dialogflow(event, vk_api)
        except ConnectionError:
            logging.warning('ConnectionError - перезапуск через 30 секунд')
            time.sleep(30)
            continue
        except Exception as E:
            logging.warning('Ошибка \n\n', E)
