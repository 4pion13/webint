import os
import asyncio
import logging
from aiogram.types import ContentType
from PIL import Image, ImageDraw
from ultralytics import YOLO

API_TOKEN = '7446114434:AAFPwCJU_O4nqNnMjcyYeo2wfKg5_xCer4o'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
model = YOLO('/Users/romannovikov/Documents/Проекты/bot/result/yolov8n_fistech_techniks_v8_50e/weights/best.pt')


def process_image(image_path):
    result = model.predict(model='/Users/romannovikov/Documents/Проекты/bot/result/yolov8n_fistech_techniks_v8_50e/weights/best.pt', source=image_path, imgsz=640, save=True, save_dir='runs/detect/predict')
    print(result)


def process_video(video_path):
    result = model.predict(model='/Users/romannovikov/Documents/Проекты/bot/result/yolov8n_fistech_techniks_v8_50e/weights/best.pt', source=video_path, imgsz=640, save=True, save_dir='runs/detect/predict')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне фото или видео, и я отмечу на них объекты.")


@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo_path = f"{message.chat.id}_{message.message_id}.jpg"
    await message.photo[-1].download(destination_file=photo_path)

    await asyncio.to_thread(process_image, photo_path)

    processed_photo_dir = 'runs/detect/predict/'
    processed_photo_path = os.path.join(processed_photo_dir, os.path.basename(photo_path))

    while not os.path.exists(processed_photo_path):
        await asyncio.sleep(1)

    if os.path.exists(processed_photo_path):
        with open(processed_photo_path, 'rb') as photo:
            await message.reply_photo(photo, caption="Вот ваше обработанное изображение!")
    else:
        await message.reply("Ошибка: не удалось найти обработанное изображение.")


@dp.message_handler(content_types=ContentType.VIDEO)
async def handle_video(message: types.Message):
    video_path = f"{message.chat.id}_{message.message_id}.avi"
    await message.video.download(destination_file=video_path)

    await asyncio.to_thread(process_video, video_path)

    processed_video_dir = 'runs/detect/predict/'
    processed_video_path = os.path.join(processed_video_dir, os.path.basename(video_path))

    while not os.path.exists(processed_video_path):
        await asyncio.sleep(1)

    if os.path.exists(processed_video_path):
        with open(processed_video_path, 'rb') as video:
            await message.reply_video(video, caption="Вот ваше обработанное видео!")
    else:
        await message.reply("Ошибка: не удалось найти обработанное видео.")


if __name__ == '__main__':
    Dispatcher.start_polling(dp, skip_updates=True)

