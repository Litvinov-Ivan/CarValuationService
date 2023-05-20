from ml.model import Model
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from pathlib import Path
import pandas as pd
import pickle


def load_model() -> Model:
    # equipment modes
    modes_path = "data/weights/equipment_modes.csv"
    path = Path(__file__).parent / modes_path
    equipment_modes = pd.read_csv(path)

    # base_price_grouper
    weights_save_path = "data/weights/base_price_grouper.csv"
    path = Path(__file__).parent / weights_save_path
    base_price_grouper = pd.read_csv(path)

    # desc w2v
    model_save_path = Path(__file__).parent / 'data/weights/desc_w2v_model'
    word_vectors_save_path = Path(__file__).parent / 'data/weights/desc_w2v_word_vectors'
    w2v_model = Word2Vec.load(str(model_save_path))
    w2v_model_wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    # desc tf-idf
    model_save_path = Path(__file__).parent / 'data/weights/desc_tfidf_model.pkl'
    with open(model_save_path, 'rb') as f:
        tfidf = pickle.load(f)

    # eq w2v
    model_save_path = Path(__file__).parent / 'data/weights/equip_w2v_model'
    word_vectors_save_path = Path(__file__).parent / 'data/weights/equip_w2v_word_vectors'
    equipment_w2v_model = Word2Vec.load(str(model_save_path))
    equipment_w2v_model_wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    # mod w2v
    model_save_path = Path(__file__).parent / 'data/weights/modification_w2v_model'
    word_vectors_save_path = Path(__file__).parent / 'data/weights/modification_w2v_word_vectors'
    modification_w2v_model = Word2Vec.load(str(model_save_path))
    modification_w2v_model_wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    features_models_dict = {
        "base_price_grouper": base_price_grouper,
        "equipment_modes": equipment_modes,
        "w2v_model": w2v_model,
        "w2v_model_wv": w2v_model_wv,
        "tfidf": tfidf,
        "eq_w2v_model": equipment_w2v_model,
        "eq_w2v_model_wv": equipment_w2v_model_wv,
        "mod_w2v_model": modification_w2v_model,
        "mod_w2v_model_wv": modification_w2v_model_wv,
    }

    model = Model(models_dict=features_models_dict)
    return model


if __name__ == "__main__":
    import time

    car = {
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

    debug_model = load_model()
    time_start = time.perf_counter()
    pred = debug_model.predict(car)
    time_end = time.perf_counter()
    print(f'predicted price - {pred}')
    print(f'time for one inference - {time_end - time_start}')


