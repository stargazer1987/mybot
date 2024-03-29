from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

from random import randint
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число { user_number}, мое {bot_number}, вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число { user_number}, мое {bot_number}, ничья"
    else:
        message = f"Ваше число { user_number}, мое {bot_number}, вы проиграли"
    return message


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Прислать котика', KeyboardButton('Мои координаты', request_location=True), 'Заполнить анкету']
    ])


# NEW VERSION
def is_cat2(url):
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    # This is how you authenticate.
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    request = service_pb2.PostModelOutputsRequest(
        # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
                resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(url=url)))
        ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))

    for concept in response.outputs[0].data.concepts:
        print('%12s: %.2f' % (concept.name, concept.value))  # Для проверки паттерна в консоле
        if concept.name == 'cat' and concept.value >= 0.95:
            return True
    else:
        return False
