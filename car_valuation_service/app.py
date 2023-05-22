import os
import asyncio
import time
from fastapi import FastAPI
from pydantic import BaseModel
from ml.datatypes import Car
from ml.model import Model
from logging import getLogger
from statsd import StatsClient


logger = getLogger()

GRAPHITE_HOST = os.environ.get('GRAPHITE_HOST', None)
GRAPHITE_PORT = os.environ.get('GRAPHITE_PORT', None)
logger.warning(f'graphite url: {GRAPHITE_HOST}, port: {GRAPHITE_PORT}')
statsd = StatsClient(GRAPHITE_HOST, int(GRAPHITE_PORT), prefix='car_valuation_service')


class Prediction(BaseModel):
    predicted_value: int


model = None
app = FastAPI()


# create a route
@app.get("/")
def index():
    return {"text": "Welcome to Car Valuation Service!"}


# Register the function to run during startup
@app.on_event("startup")
def startup_event():
    global model
    model = Model()


@app.post("/predict")
async def predict(x: Car):
    time_start = time.perf_counter()
    pred = await model.predict(x.dict())
    time_end = time.perf_counter()
    statsd.timing(f'predict_price.timing.inference_time', time_end - time_start)
    statsd.incr(f'predict_price.request_status.success.count')
    return Prediction(
        predicted_value=int(pred)
    )


if __name__ == "__main__":
    car = {
        "actual_price": 5200000.0,
        "brand": "Porsche",
        "model": "Cayenne",
        "sale_end_date": "2022-11-26 00:00:00",
        "description": "🔥🔥🔥СПЕЦПРЕДЛОЖЕНИЕ!!!🔥🔥🔥 \n\n🚙 Porsche Cayenne III\n\n    ✅ WP1ZZZ9YZKDA05407\n\n⚡ Автомобиль из Европы!!! Идеальное состояние!!!\n\n   ✅1 Владелец. ЭПТС\n   ✅Полностью в родном окрасе.\n   ✅ОТЛИЧНЫЙ ВНЕШНИЙ ВИД\n   ✅ЧИСТЫЙ УХОЖЕННЫЙ САЛОН\n   ✅АВТОМОБИЛЬ ПРОШЕЛ КОМПЛЕКСНУЮ И КРИМИНАЛИСТИЧЕСКУЮ ДИАГНОСТИКУ\n\n💥 СОСТОЯНИЕ НОВОГО АВТОМОБИЛЯ!💥\n\nДилерский центр АУДИ ЦЕНТР ВОСТОК удобно расположен на Востоке Москвы, 2км от МКАД. \n\nНам важно, чтобы при покупке автомобиля Вы чувствовали себя максимально защищенными!\n\n🔁Продайте или обменяйте свой автомобиль на персональных условиях!\n\nОсмотр ежедневно с 9:00 до 21:00, без перерыва и выходных.\nДо встречи в АУДИ ЦЕНТР ВОСТОК!\n\nПТС оригинал.\n\nМесто осмотра\n\nОсмотреть автомобиль можно по адресу: Московская область, Балашиха, ш. Энтузиастов, д. 12Б.\n\nКомплектация «Cayenne Platinum Edition»:\n\nАктивная безопасность:\n— Антиблокировочная система\n— Антипробуксовочная система\n— Система курсовой устойчивости\n— Система помощи при экстренном торможении\n— Датчик давления в шинах\n— ЭРА-ГЛОНАСС\nПассивная безопасность:\n— Подушки безопасности водителя с защитой коленей\n— Подушки безопасности пассажира\n— Боковые передние подушки безопасности\n— Оконные шторки безопасности\n— Блокировка замков задних дверей\n— Система крепления детских автокресел\nПротивоугонная система:\n— Сигнализация с обратной связью\n— Датчик проникновения в салон (датчик объема)\n— Иммобилайзер\n— Центральный замок\nПомощь при вождении:\n— Бортовой компьютер\n— Круиз-контроль\n— Парктроник передний и задний\n— Система помощи при старте в гору\n— Система помощи при спуске с горы\n— Система управления дальним светом\n— Датчик света\n— Датчик дождя\nКомфорт:\n— Активный усилитель руля\n— Запуск двигателя с кнопки\n— Система “старт-стоп”\n— Система доступа без ключа\n— Доводчик дверей\n— Регулировка руля\n— Электрорегулировка сиденья водителя с памятью положения\n— Электрорегулировка сиденья пассажира\n— Электростеклоподъемники передние и задние\n— Электропривод зеркал\n— Электропривод крышки багажника\nУправление климатом и обогрев:\n— Климат-контроль 2-зонный\n— Подогрев сидений водителя и пассажира\n— Подогрев руля\n— Обогрев зеркал\nМультимедиа и навигация:\n— Навигационная система\n— CD\n— USB\n— TV\n— Функция Apple CarPlay\n— Функция Android Auto\n— Голосовое управление\n— Bluetooth\n— Мультифункциональное рулевое колесо\n— Розетка 12V\nСалон и интерьер:\n— Кожаная обивка салона\n— Отделка кожей рычага КПП\n— Кожаный руль\n— Панорамная крыша\n— Спортивные передние сидения\n— Третий задний подголовник\n— Передний центральный подлокотник\n— Подрулевые лепестки переключения передач\n— Накладки на пороги\nЭкстерьер:\n— Размер дисков 21″\n— Тонированные стекла\nОсвещение:\n— Светодиодные фары\n— Адаптивные фары\n— Огни дневного хода\n— Корректор фар\nКомплектность:\n— Отметки ТО Частично\n— ПТС\n— Свидетельство о регистрации\n— 2 комплекта ключей\n— Докатка",
        "year": 2018,
        "generation": "III (2017—2023)",
        "body_type": "Внедорожник",
        "equipment": "Cayenne",
        "modification": "3.0 4WD AT (340 л.с.)",
        "drive_type": "Полный",
        "transmission_type": "Автомат",
        "engine_type": "Бензин",
        "doors_number": 5,
        "color": "Чёрный",
        "pts": "Оригинал",
        "owners_count": "1",
        "mileage": 106406,
        "latitude": 55.796339,
        "longitude": 37.938199
    }

    debug_model = Model()
    pred = asyncio.run(debug_model.predict(car))
    print(f'predicted price - {pred}')
