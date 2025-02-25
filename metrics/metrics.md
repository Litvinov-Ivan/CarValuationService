# Схема и метрики

## Схема решения и метрики

Нарисуйте схему решения и зафиксируйте ожидаемые метрики. В ответ 
вставьте ссылку на папку в проекте, где будет хранится решение этого 
этапа.

**1) Решение с примером использования.**

*Пример. В качестве решения проблемы необходимо разработать сервис
 определения номера с фотографии авто. Пользователь загружает фотографии
 авто, с фотографии вырезается и распознается номер, по номеру находится
 VIN. Если указанный пользователем VIN с ним не совпадает, объявление 
отклоняется.*

В качестве решения проблемы необходимо разработать сервис определения рыночной цены автомобиля по его данным. Пользователь указывает данные о своей машине, и эта информацию используется моделью для предсказания. Предсказанная рыночная цена показывается продавцу при создании объявления, а также в выдаче объявлений появится значок о рыночной цене, помогающий покупателям соориентироваться на рынке авто.

**2) Какая бизнес-метрика должна оптимизироваться? Какое её значение будет считаться успехом?**

*Пример. Мы должны не допускать подложность номеров, поэтому, чем 
больше недобросовестных пользователей мы найдем, тем лучше. С другой 
стороны, мы не должны отклонять объявления честных продавцов по причине 
неточности модели.*

*Предлагается зафиксировать абсолютное количество ложных 
срабатываний < 2 в сутки и при такой метрике максимизировать долю 
правильно найденных подложных VIN номеров.*

1. Будем использовать прокси метрику: уменьшение среднего времени закрытия объявления считаем показателем того, что люди удовлетворены сервисом. 
2. Неправильное определение рыночной цены необходимо свести к минимуму. Это связано с тем, что показ ошибочной цены для конечного пользователя может оттолкнуть его от пользования нашим сервисом. Для этого можно отслеживать активность при создании объявления (например изменение цены и жалобы) - если продавец не согласен с предложенной оценкой, это будет сигнализировать о неадекватной оценке модели. Оценку адекватности со стороны покупателей будем проводить с помощью отзывов на открытое объявление.
3. Авито зарабатывает с платных объявлений, поэтому важно увеличение количества сделок. Количество сделок зависит от количества продавцов и покупателей.

**3) Какая метрика машинного обучения будет наилучшим образом отражать оптимизацию бизнес-метрики?**

*Пример. Мы можем использовать автоматический подбор порога, 
исходя из требований по точности, и стремиться к максимальной полноте.*

Будем использовать следующие метрики, отражающие оптимизацию бизнес-метрики:

1. Метрика точности предсказаний в среднем: процентные ошибки, т.к. цены в разном диапазоне, допустим возьмём медиану (или можно взять другой квантиль) потому, что она не учитывает выбросы.
2. Для учёта выбросов воспользуемся метрикой критически неправильных оценок машин: когда цена слишком ошибочна, например процентная ошибка больше 20%, мы посчитаем количество таких ошибок.
