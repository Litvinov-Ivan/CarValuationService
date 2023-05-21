import pandas as pd
import re
import time


def preprocess_text(text):
    text = re.findall('[^\W_]+', text)
    text = [token.lower() for token in text if len(token) > 1]
    text = " ".join(text)
    if len(text) == 0:
        return 'placeholder text'
    return text


def lemmatize(text, models_dict: dict):
    lemmatizer = models_dict['lemmatizer']
    time_class_init = time.time()
    lemmas = " ".join([lemmatizer.parse(word)[0].normal_form for word in text.split()])
    time_end = time.time()
    print(f"time to lemmatize text: {time_end - time_class_init} seconds")
    return lemmas


def lemmatize_description(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    preprocess_start = time.time()
    df['description'] = df.description.apply(preprocess_text)
    preprocess_end = time.time()
    df['lemmatized_description'] = df.description.apply(lambda x: lemmatize(x, models_dict))
    lemm_end = time.time()

    print("********* lemmatization func execution time analysis *********")
    print(f"description preprocessing - {preprocess_end - preprocess_start} seconds")
    print(f"lemmatization - {lemm_end - preprocess_end} seconds")
    print("******************")
    return df


if __name__ == "__main__":
    from joblib import Parallel, delayed
    from tqdm import tqdm
    import pymorphy2


    text = "🔥🔥🔥СПЕЦПРЕДЛОЖЕНИЕ!!!🔥🔥🔥 \n\n🚙 Porsche Cayenne III\n\n    ✅ WP1ZZZ9YZKDA05407\n\n⚡ Автомобиль из Европы!!! Идеальное состояние!!!\n\n   ✅1 Владелец. ЭПТС\n   ✅Полностью в родном окрасе.\n   ✅ОТЛИЧНЫЙ ВНЕШНИЙ ВИД\n   ✅ЧИСТЫЙ УХОЖЕННЫЙ САЛОН\n   ✅АВТОМОБИЛЬ ПРОШЕЛ КОМПЛЕКСНУЮ И КРИМИНАЛИСТИЧЕСКУЮ ДИАГНОСТИКУ\n\n💥 СОСТОЯНИЕ НОВОГО АВТОМОБИЛЯ!💥\n\nДилерский центр АУДИ ЦЕНТР ВОСТОК удобно расположен на Востоке Москвы, 2км от МКАД. \n\nНам важно, чтобы при покупке автомобиля Вы чувствовали себя максимально защищенными!\n\n🔁Продайте или обменяйте свой автомобиль на персональных условиях!\n\nОсмотр ежедневно с 9:00 до 21:00, без перерыва и выходных.\nДо встречи в АУДИ ЦЕНТР ВОСТОК!\n\nПТС оригинал.\n\nМесто осмотра\n\nОсмотреть автомобиль можно по адресу: Московская область, Балашиха, ш. Энтузиастов, д. 12Б.\n\nКомплектация «Cayenne Platinum Edition»:\n\nАктивная безопасность:\n— Антиблокировочная система\n— Антипробуксовочная система\n— Система курсовой устойчивости\n— Система помощи при экстренном торможении\n— Датчик давления в шинах\n— ЭРА-ГЛОНАСС\nПассивная безопасность:\n— Подушки безопасности водителя с защитой коленей\n— Подушки безопасности пассажира\n— Боковые передние подушки безопасности\n— Оконные шторки безопасности\n— Блокировка замков задних дверей\n— Система крепления детских автокресел\nПротивоугонная система:\n— Сигнализация с обратной связью\n— Датчик проникновения в салон (датчик объема)\n— Иммобилайзер\n— Центральный замок\nПомощь при вождении:\n— Бортовой компьютер\n— Круиз-контроль\n— Парктроник передний и задний\n— Система помощи при старте в гору\n— Система помощи при спуске с горы\n— Система управления дальним светом\n— Датчик света\n— Датчик дождя\nКомфорт:\n— Активный усилитель руля\n— Запуск двигателя с кнопки\n— Система “старт-стоп”\n— Система доступа без ключа\n— Доводчик дверей\n— Регулировка руля\n— Электрорегулировка сиденья водителя с памятью положения\n— Электрорегулировка сиденья пассажира\n— Электростеклоподъемники передние и задние\n— Электропривод зеркал\n— Электропривод крышки багажника\nУправление климатом и обогрев:\n— Климат-контроль 2-зонный\n— Подогрев сидений водителя и пассажира\n— Подогрев руля\n— Обогрев зеркал\nМультимедиа и навигация:\n— Навигационная система\n— CD\n— USB\n— TV\n— Функция Apple CarPlay\n— Функция Android Auto\n— Голосовое управление\n— Bluetooth\n— Мультифункциональное рулевое колесо\n— Розетка 12V\nСалон и интерьер:\n— Кожаная обивка салона\n— Отделка кожей рычага КПП\n— Кожаный руль\n— Панорамная крыша\n— Спортивные передние сидения\n— Третий задний подголовник\n— Передний центральный подлокотник\n— Подрулевые лепестки переключения передач\n— Накладки на пороги\nЭкстерьер:\n— Размер дисков 21″\n— Тонированные стекла\nОсвещение:\n— Светодиодные фары\n— Адаптивные фары\n— Огни дневного хода\n— Корректор фар\nКомплектность:\n— Отметки ТО Частично\n— ПТС\n— Свидетельство о регистрации\n— 2 комплекта ключей\n— Докатка"
    text = preprocess_text(text)

    texts = text.split()
    batch_size = len(texts)

    text_batch = [texts[i: i + batch_size] for i in range(0, len(texts), batch_size)]

    """#processed_texts = Parallel(n_jobs=2)(delayed(lemmatize)(t) for t in tqdm(text_batch))
    # print(f"time to lemmatize text: {time_end - time_start} seconds")
    m = Mystem()
    time_start = time.time()
    lemm_text = m.lemmatize(text)
    time_end = time.time()
    print(f"time to lemmatize: {time_end - time_start} seconds")"""
    lemma = pymorphy2.MorphAnalyzer()

    def preprocess_text(texts):
        text = " ".join([lemma.parse(word)[0].normal_form for word in texts])
        return text


    time_start = time.time()

    preprocc_text = preprocess_text(texts)
    time_end = time.time()
    print(f"time to lemmatize: {time_end - time_start} seconds")



