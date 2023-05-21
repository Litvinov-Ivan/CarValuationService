from ml.model import Model
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from pathlib import Path
from reverse_geocode import GeocodeData
from pymorphy2 import MorphAnalyzer
import pandas as pd
import pickle


def load_model() -> Model:
    # geocode class init
    geocode_class_instance = GeocodeData()

    # lemmatizer init
    lemmatizer = MorphAnalyzer()

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
        "geocode_class_instance": geocode_class_instance,
        "lemmatizer": lemmatizer,
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
    import asyncio
    import warnings
    warnings.simplefilter("ignore")

    car =  {"actual_price": 1418040.0,
 "brand": "Toyota",
 "model": "Corolla",
 "sale_end_date": "2022-08-21 00:00:00",
 "description": "✅ отличное техническое состояние\n✅ отличное состояние кузова\n\n✅ родной пробег (подтвержденный автотекой)\n✅ Автомобиль прошёл полную техническую проверку и готов к эксплуатации\n✅ Автомобиль выкуплен и находится в собственности компании.\n✅ Отличное состояние автомобиля\n✅ ПТС оригинал\n✅ 3 владельца\n✅ Полностью заводской окрас \n✅ Без участия в ДТП\n\n✅ Автомобиль прошел полную проверку и готов к эксплуатации\n\n➕ Отделка салона -  ткань\n➕ Система облегчения парковки (камера заднего вида)\n➕ Система предупреждения о падении давления в шинах\n➕ Аудиосистема \n➕ Климат-контроль\n➕ Декоративные элементы салона из алюминия\n➕ Подогрев передних сидений\nКомплектация:\n\n➕ Подогрев сидений водителя и пассажира\n➕ Обогрев зеркал\n➕ Климат-контроль\n➕ Антиблокировочная система\n➕ Антипробуксовочная система\n➕ Подушки безопасности водителя\n➕ Подушки безопасности пассажира\n➕ Боковые передние и задние подушки безопасности\n➕ Иммобилайзер\n➕ Центральный замок\n➕ Бортовой компьютер\n➕ Круиз-контроль\n➕ Датчик света\n➕ Датчик дождя\n➕ Усилитель руля\n➕ Регулировка руля в двух плоскостях\n➕ Электростеклоподъемники передние и задние\n➕ Электропривод зеркал\n➕ Литые легкосплавные диски\n➕ Тонированные стекла\n➕ Омыватель фар\n➕ Датчики парковки\n\n✅ Все наши автомобили находятся в теплом помещении \n✅ Проводим тест-драйв перед приобретением на любом автомобиле.\nУважаемые наши Клиенты, каждый понравившийся Вам автомобиль вы можете абсолютно бесплатно и без очереди проверить.\nДля Вас мы предоставляем:\n🔧 Проверка толщины краски кузова автомобиля\n🔧 Проверка подвески\n🔧 Проверка работоспособности системы кондиционирования автомобиля.\n\n🟢 Честный пробег - Мы не корректируем пробеги\n🟢 Гарантированная выгода при обмене вашего автомобиля\n🟢 Специальные предложения по кредитованию и страхованию\n🟢 Мы гарантируем юридическую чистоту автомобиля\n🟢 Есть возможность провести тест-драйв\n🟢 Автомобиль прошел комплексную предпродажную подготовку\n\nСтаньте владельцем автомобиля уже сегодня! Звоните!\n\nПонравился этот автомобиль? До 30.08.2022 на него действует специальное предложение при обмене и покупке в кредит. Успей воспользоваться выгодой раньше остальных! \n\nКЛЮЧАВТО | Автомобили с пробегом:\n- дважды победитель в номинации “Автодилер года” по версии Автостат;\n- более 800 000 авто продано;\n- 5 000 автомобилей на сайте;\n- 106 автосалонов по России;\n- 21 год на рынке.\n\nАвтокредит от 6,4%!!! Успейте купить машину на выгодных условиях! \n\nЧтобы получить предложение, напишите сообщение 'Хочу автокредит!'\n\nКЛЮЧАВТО | Автомобили с пробегом:\n- более 15 надёжных банков-партнёров России по версии Forbes 2022;\n- кредит без первоначального взноса;\n- оформление по двум документам;\n- полное сопровождение сделки;\n- индивидуальный подход в выборе условий кредитования;\n- кредитуем все регионы Российской Федерации;\n- страхование КАСКО в 10 ведущих страховых компаниях на лучших партнёрских условиях для вас 🤝;\n- страхование ОСАГО без дополнительных комиссий!\n\n* Подробности в отделе продаж\n\nПТС оригинал.\n\nМесто осмотра\n\nОсмотреть автомобиль можно по адресу: Пермь, ул. Спешилова, 111/3, КЛЮЧАВТО | Автомобили с пробегом Пермь\n\nХарактеристики\n— Вариаторная коробка передач\nКомплектация:\n\nАктивная безопасность:\n— Антиблокировочная система\nПассивная безопасность:\n— Подушки безопасности водителя\n— Подушки безопасности пассажира\n— Боковые передние подушки безопасности\n— Система крепления детских автокресел\nПротивоугонная система:\n— Иммобилайзер\n— Центральный замок\nКомфорт:\n— Усилитель руля\n— Регулировка руля\n— Регулировка сиденья водителя в двух плоскостях\n— Электростеклоподъемники передние и задние\n— Электропривод зеркал\nУправление климатом и обогрев:\n— Кондиционер\n— Подогрев сидений водителя и пассажира\n— Подогрев руля\n— Обогрев зеркал\nМультимедиа и навигация:\n— CD\n— USB\n— AUX\n— Аудиоподготовка\n— Мультифункциональное рулевое колесо\nСалон и интерьер:\n— Тканевая обивка салона\n— Кожаный руль\n— Складывающееся заднее сидение\n— Передний центральный подлокотник\nЭкстерьер:\n— Размер дисков 16″\nОсвещение:\n— Противотуманные фары\nКомплектность:\n— Запасное колесо",
 "year": 2018,
 "generation": "XI рестайлинг (2015—2019)",
 "body_type": "Седан",
            "equipment": None,
 "modification": "1.6 CVT (122 л.с.)",
 "drive_type": "Передний",
 "transmission_type": "Вариатор",
 "engine_type": "Бензин",
 "doors_number": 4,
 "color": "Серый",
 "pts": "Оригинал",
 "owners_count": "3",
 "mileage": 56600,
 "latitude": 58.010374,
 "longitude": 56.228398}

    debug_model = load_model()
    pred = asyncio.run(debug_model.predict(car))

    print(f'predicted price - {pred}')
