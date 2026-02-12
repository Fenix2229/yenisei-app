from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    Epoch, HistoricalEvent, GeographicPoint, 
    GalleryImage, QuizQuestion, InterestingFact
)

def clear_database():
    """Очистить все таблицы"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ База данных очищена и пересоздана")

def seed_epochs(db: Session):
    """Создать исторические эпохи"""
    epochs = [
        Epoch(
            name="Древний период и палеолит",
            start_year=-30000,
            end_year=1500,
            description="Первые следы человеческой цивилизации на берегах Енисея. Стоянки древних людей, петроглифы и священные места коренных народов Сибири.",
            color="#8B4513",
            order_index=1
        ),
        Epoch(
            name="Эпоха русских первопроходцев",
            start_year=1600,
            end_year=1750,
            description="Освоение Сибири казаками, основание острогов и первых поселений. Енисей становится главной транспортной артерией региона.",
            color="#D97706",
            order_index=2
        ),
        Epoch(
            name="Золотая лихорадка и индустриализация",
            start_year=1750,
            end_year=1917,
            description="Открытие золотых приисков, развитие торговли и промышленности. Строительство Транссибирской магистрали.",
            color="#F59E0B",
            order_index=3
        ),
        Epoch(
            name="Советский период",
            start_year=1917,
            end_year=1991,
            description="Индустриализация Сибири, строительство гидроэлектростанций, создание Норильского промышленного района. Енисей становится энергетическим центром СССР.",
            color="#EF4444",
            order_index=4
        ),
        Epoch(
            name="Современная эпоха",
            start_year=1991,
            end_year=2026,
            description="Экологические вызовы, развитие туризма, сохранение природного наследия. Енисей в XXI веке.",
            color="#3B82F6",
            order_index=5
        )
    ]
    
    db.add_all(epochs)
    db.commit()
    print(f"✅ Добавлено {len(epochs)} эпох")
    return epochs

def seed_historical_events(db: Session, epochs):
    """Создать исторические события"""
    events = [
        # Древний период
        HistoricalEvent(
            epoch_id=epochs[0].id,
            title="Стоянка Афонтова Гора",
            year=-20000,
            date_description="около 20000 лет до н.э.",
            description="Одна из древнейших стоянок человека на территории Сибири. Археологические раскопки обнаружили орудия труда, украшения и следы жилищ палеолитических охотников. Стоянка расположена на правом берегу Енисея в черте современного Красноярска. Находки свидетельствуют о высоком уровне культуры древних обитателей этих мест.",
            short_description="Древнейшая стоянка человека на Енисее, 20 тысяч лет до н.э.",
            image_url="https://avatars.mds.yandex.net/get-altay/15487932/2a000001981b8f780d71be3a59bbaec87b53/orig",
            image_caption="Афонтова Гора во всем своем величии",
            importance=9
        ),
        HistoricalEvent(
            epoch_id=epochs[0].id,
            title="Петроглифы Шалаболинской писаницы",
            year=-3000,
            date_description="3-е тысячелетие до н.э.",
            description="Уникальный памятник наскального искусства на правом берегу Енисея. Более 100 рисунков изображают сцены охоты, ритуальные действия, животных и солярные символы. Петроглифы созданы древними народами, населявшими берега реки. Это одно из крупнейших скоплений наскальных изображений в Сибири.",
            short_description="Древние наскальные рисунки на берегу Енисея",
            image_url="https://cs14.pikabu.ru/post_img/2023/08/12/6/og_og_16918313092388722.jpg",
            image_caption="Петроглифы на скалах Енисея",
            importance=8
        ),
        HistoricalEvent(
            epoch_id=epochs[0].id,
            title="Поселения хакасов и кетов",
            year=500,
            date_description="V-XV века н.э.",
            description="На берегах Енисея формируются поселения коренных народов Сибири — хакасов, кетов, эвенков. Река становится основой их жизненного уклада: рыболовство, охота, торговля. Кеты считаются древнейшим народом региона, их язык не имеет родственных связей с другими языковыми группами. Хакасы создали развитую культуру скотоводства и земледелия.",
            short_description="Формирование культур коренных народов Енисея",
            image_url="https://avatars.mds.yandex.net/i?id=90afc08960180b5a509047d1ab39dd8e_l-4589919-images-thumbs&n=13",
            image_caption="Традиционное жилище народов Сибири",
            importance=7
        ),
        
        # Эпоха первопроходцев
        HistoricalEvent(
            epoch_id=epochs[1].id,
            title="Основание Енисейска",
            year=1619,
            date_description="1619 год",
            description="Казачий атаман Петр Албычев и Черкас Рукин основали Енисейский острог — первый русский город на Енисее. Острог стал опорным пунктом освоения Восточной Сибири и Дальнего Востока. Отсюда снаряжались экспедиции к Байкалу, Лене и Тихому океану. Енисейск долгое время был административным и торговым центром огромного региона.",
            short_description="Основание первого русского города на Енисее",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Сибирь._Енисейск._Вид_с_реки._1900-е_гг_ГИМ_e1t3.jpg/500px-Сибирь._Енисейск._Вид_с_реки._1900-е_гг_ГИМ_e1t3.jpg",
            image_caption="Историческая реконструкция острога",
            importance=10
        ),
        HistoricalEvent(
            epoch_id=epochs[1].id,
            title="Экспедиция Семёна Дежнёва",
            year=1648,
            date_description="1648 год",
            description="Из Енисейска отправилась знаменитая экспедиция Семёна Дежнёва, которая впервые обогнула Чукотку и открыла пролив между Азией и Америкой. Енисей служил отправной точкой для многих великих географических открытий XVII века. Казаки использовали реку как главную транспортную магистраль для продвижения на восток.",
            short_description="Енисей — отправная точка великих открытий",
            image_url="https://news.store.rambler.ru/img/834080dc7355a1956cd711f9ce4b6f35?img-format=auto&img-1-resize=height:350,fit:max&img-2-filter=sharpen",
            image_caption="Северные просторы Сибири",
            importance=9
        ),
        HistoricalEvent(
            epoch_id=epochs[1].id,
            title="Основание Красноярского острога",
            year=1628,
            date_description="1628 год",
            description="Воевода Андрей Дубенский основал Красноярский острог на месте слияния Качи и Енисея. Острог строился как военное укрепление для защиты от набегов и как база для дальнейшего освоения региона. Красноярск быстро превратился в важный торговый и культурный центр. Сегодня это крупнейший город на Енисее.",
            short_description="Основание Красноярска — будущего сибирского гиганта",
            image_url="https://avatars.mds.yandex.net/i?id=644787708f758e894006d9eebf7d0a77_l-5363089-images-thumbs&n=13",
            image_caption="Панорама исторического Красноярска",
            importance=10
        ),
        
        # Золотая лихорадка
        HistoricalEvent(
            epoch_id=epochs[2].id,
            title="Открытие золота в Енисейской тайге",
            year=1830,
            date_description="1830-е годы",
            description="Обнаружение золотых месторождений в бассейне Енисея вызвало настоящую золотую лихорадку. Тысячи старателей устремились в Сибирь. Возникли золотые прииски, поселки и целые города. Добыча золота стала основой экономики региона на десятилетия. Енисей превратился в главную транспортную артерию для доставки золота в центральную Россию.",
            short_description="Начало золотой лихорадки на Енисее",
            image_url="https://my.krskstate.ru/upload/iblock/4fc/zoloto_07.jpg",
            image_caption="Золотые прииски Сибири",
            importance=8
        ),
        HistoricalEvent(
            epoch_id=epochs[2].id,
            title="Развитие пароходства",
            year=1863,
            date_description="1863 год",
            description="На Енисее началось регулярное пароходное сообщение. Первые пароходы связали Красноярск с северными районами и Енисейском. Это революционизировало транспортную систему региона, ускорило торговлю и развитие промышленности. К концу XIX века по Енисею курсировало несколько десятков пароходов, перевозивших грузы и пассажиров.",
            short_description="Появление пароходов на Енисее",
            image_url="https://static.tildacdn.com/tild3764-3337-4335-b363-393265663261/__1863_.jpeg",
            image_caption="Пароход на сибирской реке",
            importance=7
        ),
        HistoricalEvent(
            epoch_id=epochs[2].id,
            title="Строительство Транссибирской магистрали",
            year=1895,
            date_description="1895 год",
            description="Через Енисей был построен железнодорожный мост — крупнейшее инженерное сооружение того времени в России. Мост соединил западную и восточную части Транссибирской магистрали. Проект моста получил Гран-при на Всемирной выставке в Париже в 1900 году. Это событие открыло новую эру в развитии Сибири и Енисейского края.",
            short_description="Строительство моста через Енисей",
            image_url="https://avatars.mds.yandex.net/i?id=40aa85f9ec2c7228c2f47a722c02c0a3b35d57cc-5665918-images-thumbs&n=13",
            image_caption="Исторический мост через Енисей",
            importance=10
        ),
        
        # Советский период
        HistoricalEvent(
            epoch_id=epochs[3].id,
            title="Открытие Норильского месторождения",
            year=1921,
            date_description="1921 год",
            description="Геолог Николай Урванцев открыл богатейшие месторождения никеля, меди и других металлов в районе Норильска. Это стало началом освоения Крайнего Севера. Енисей служил главной транспортной артерией для доставки грузов и оборудования. В 1935 году началось строительство Норильского горно-металлургического комбината.",
            short_description="Открытие норильских месторождений",
            image_url="https://avatars.mds.yandex.net/i?id=f8e4931f692ef32368917f11dd23976f2d64a123-5452154-images-thumbs&n=13",
            image_caption="Место открытия норильских богатств",
            importance=9
        ),
        HistoricalEvent(
            epoch_id=epochs[3].id,
            title="Строительство Красноярской ГЭС",
            year=1955,
            date_description="1955-1972 годы",
            description="Началось строительство одной из крупнейших гидроэлектростанций в мире. Красноярская ГЭС стала символом индустриальной мощи СССР. Высота плотины — 124 метра, мощность — 6000 МВт. Строительство потребовало перекрытия могучего Енисея и создания огромного водохранилища. ГЭС обеспечила электроэнергией весь регион и стала градообразующим предприятием.",
            short_description="Строительство Красноярской ГЭС — энергетического гиганта",
            image_url="https://avatars.mds.yandex.net/i?id=39bfd2ff19f23d3b9035a61f417cb22187557b2b-5361789-images-thumbs&n=13",
            image_caption="Плотина Красноярской ГЭС",
            importance=10
        ),
        HistoricalEvent(
            epoch_id=epochs[3].id,
            title="Саяно-Шушенская ГЭС",
            year=1963,
            date_description="1963-1985 годы",
            description="Строительство крупнейшей по мощности электростанции России в верховьях Енисея. Высота арочно-гравитационной плотины — 245 метров. Станция расположена в живописном каньоне между Саянских гор. Строительство продолжалось 22 года и стало выдающимся инженерным достижением. В 2009 году произошла крупная авария, после которой станция была полностью восстановлена.",
            short_description="Саяно-Шушенская ГЭС — крупнейшая в России",
            image_url="https://avatars.mds.yandex.net/i?id=dd0e916fcc16b2452cd82d2ec2e94057f8534af2-5876235-images-thumbs&n=13",
            image_caption="Грандиозная плотина в Саянах",
            importance=10
        ),
        HistoricalEvent(
            epoch_id=epochs[3].id,
            title="Красноярск-26 (Железногорск)",
            year=1950,
            date_description="1950 год",
            description="В 60 км от Красноярска началось строительство секретного города для производства оружейного плутония. Город был полностью закрыт, его не было на картах. Енисей использовался для охлаждения ядерных реакторов. Город обеспечивал ядерную программу СССР. В 1992 году получил официальное название Железногорск и был частично открыт.",
            short_description="Создание секретного атомного города",
            image_url="https://avatars.mds.yandex.net/i?id=23b95fc69d07b67d5aa266cbfa1a9f1c-5220681-images-thumbs&n=13",
            image_caption="Атомная промышленность на Енисее",
            importance=8
        ),
        
        # Современная эпоха
        HistoricalEvent(
            epoch_id=epochs[4].id,
            title="Экологические проблемы Енисея",
            year=1995,
            date_description="1990-е годы",
            description="После распада СССР стали очевидны масштабы экологических проблем Енисея: загрязнение промышленными стоками, радиоактивное загрязнение от атомных производств, деградация рыбных запасов. Начались программы по очистке реки и восстановлению экосистем. Создаются заповедники и природные парки. Вопрос экологии Енисея стал общенациональной проблемой.",
            short_description="Осознание экологических проблем великой реки",
            image_url="https://avatars.mds.yandex.net/i?id=53cb95925f5507f8055eaa6fe7f40a197d1f06a4-7553521-images-thumbs&n=13",
            image_caption="Экология Енисея требует внимания",
            importance=7
        ),
        HistoricalEvent(
            epoch_id=epochs[4].id,
            title="Развитие туризма на Енисее",
            year=2000,
            date_description="2000-е годы",
            description="Енисей становится популярным туристическим направлением. Развиваются круизы по реке, экологический туризм, сплавы. Туристы приезжают увидеть Столбы, Красноярское водохранилище, дикую тайгу и горы Саян. Создается инфраструктура для приема гостей. Енисей открывается как уникальная природная достопримечательность мирового уровня.",
            short_description="Енисей — новый туристический маршрут",
            image_url="https://avatars.mds.yandex.net/i?id=55899673d0fe34b561fda8c2bfeb08b5bcf4f57c-5700821-images-thumbs&n=13",
            image_caption="Туризм на Енисее",
            importance=6
        ),
        HistoricalEvent(
            epoch_id=epochs[4].id,
            title="Енисей в XXI веке",
            year=2020,
            date_description="2020-е годы",
            description="Сегодня Енисей — это одна из величайших рек планеты, символ Сибири и важнейшая водная артерия России. Река обеспечивает водой миллионы людей, вырабатывает электроэнергию, служит транспортным путем. Стоят задачи сохранения уникальной природы, развития экономики региона и улучшения экологической ситуации. Енисей остается сердцем Сибири.",
            short_description="Енисей сегодня — великая река современной России",
            image_url="https://avatars.mds.yandex.net/i?id=230e8af300548b62b4ae7859616e22236213f674-16558525-images-thumbs&n=13",
            image_caption="Современный Енисей",
            importance=8
        )
    ]
    
    db.add_all(events)
    db.commit()
    print(f"✅ Добавлено {len(events)} исторических событий")

def seed_geographic_points(db: Session):
    """Создать географические точки"""
    points = [
        # Города
        GeographicPoint(
            name="Кызыл",
            type="city",
            latitude=51.7191,
            longitude=94.4437,
            description="Столица Республики Тыва, город у истоков Енисея. Здесь Большой Енисей и Малый Енисей сливаются в единую реку. В центре города установлен обелиск 'Центр Азии'. Население около 120 тысяч человек.",
            short_description="Столица Тывы, город у истоков Енисея",
            founding_year=1914,
            population=120000,
            image_url="https://images.unsplash.com/photo-1519817914152-22d216bb9170",
            icon="city",
            color="#EF4444"
        ),
        GeographicPoint(
            name="Абакан",
            type="city",
            latitude=53.7215,
            longitude=91.4425,
            description="Столица Республики Хакасия, город на берегу Енисея. Крупный промышленный и культурный центр Южной Сибири. Рядом находятся древние курганы и археологические памятники. Население около 180 тысяч человек.",
            short_description="Столица Хакасии на берегу Енисея",
            founding_year=1931,
            population=180000,
            image_url="https://images.unsplash.com/photo-1477959858617-67f85cf4f1df",
            icon="city",
            color="#EF4444"
        ),
        GeographicPoint(
            name="Красноярск",
            type="city",
            latitude=56.0153,
            longitude=92.8932,
            description="Крупнейший город на Енисее, миллионник, столица Красноярского края. Основан в 1628 году как острог. Крупный промышленный, научный и культурный центр Сибири. Город разделен Енисеем на две части, соединенные множеством мостов.",
            short_description="Миллионный город, сердце Сибири",
            founding_year=1628,
            population=1100000,
            image_url="https://images.unsplash.com/photo-1513366976276-090a286e6334",
            icon="city",
            color="#DC2626"
        ),
        GeographicPoint(
            name="Дивногорск",
            type="city",
            latitude=55.9572,
            longitude=92.3765,
            description="Город гидростроителей, построенный для строительства Красноярской ГЭС. Расположен на берегу Красноярского водохранилища. Отсюда открываются живописные виды на Енисей и окружающие горы. Популярное место для туризма и отдыха.",
            short_description="Город гидростроителей у Красноярской ГЭС",
            founding_year=1957,
            population=32000,
            image_url="https://images.unsplash.com/photo-1464207687429-7505649dae38",
            icon="city",
            color="#F97316"
        ),
        GeographicPoint(
            name="Енисейск",
            type="city",
            latitude=58.4494,
            longitude=92.1752,
            description="Один из старейших городов Сибири, основан в 1619 году. Исторический центр освоения Восточной Сибири. Сохранилась уникальная деревянная и каменная архитектура XVII-XIX веков. Включен в список исторических городов России.",
            short_description="Первый русский город на Енисее (1619)",
            founding_year=1619,
            population=18000,
            image_url="https://images.unsplash.com/photo-1548198138-f26767e0b4f3",
            icon="city",
            color="#F59E0B"
        ),
        GeographicPoint(
            name="Лесосибирск",
            type="city",
            latitude=58.2343,
            longitude=92.4833,
            description="Центр лесной промышленности Красноярского края. Город расположен на берегу Енисея в окружении бескрайней тайги. Крупнейший производитель древесины в регионе. Живописная природа и суровый климат.",
            short_description="Центр лесной промышленности",
            founding_year=1975,
            population=62000,
            image_url="https://images.unsplash.com/photo-1448375240586-882707db888b",
            icon="city",
            color="#F97316"
        ),
        GeographicPoint(
            name="Игарка",
            type="city",
            latitude=67.4667,
            longitude=86.5833,
            description="Город-порт за Полярным кругом. Один из самых северных городов России. Основан как центр лесоэкспорта. Знаменит вечной мерзлотой и музеем, построенным в толще мерзлого грунта. Навигация по Енисею — всего 3 месяца в году.",
            short_description="Полярный город-порт на Енисее",
            founding_year=1929,
            population=4500,
            image_url="https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5",
            icon="city",
            color="#3B82F6"
        ),
        GeographicPoint(
            name="Дудинка",
            type="city",
            latitude=69.4056,
            longitude=86.1778,
            description="Самый северный город на Енисее и один из самых северных портов мира. Административный центр Таймыра. Отсюда начинается Северный морской путь. Население около 22 тысяч человек. Город многонационален: русские, долганы, ненцы, нганасаны.",
            short_description="Самый северный порт на Енисее",
            founding_year=1667,
            population=22000,
            image_url="https://images.unsplash.com/photo-1519904981063-b0cf448d479e",
            icon="city",
            color="#1E40AF"
        ),
        
        # Природные достопримечательности
        GeographicPoint(
            name="Национальный парк 'Красноярские Столбы'",
            type="nature",
            latitude=55.9333,
            longitude=92.7667,
            description="Уникальный природный парк со скалами-останцами причудливых форм. Высота столбов достигает 100 метров. Популярное место для скалолазания и туризма. Возраст скал — около 600 миллионов лет. Объект всемирного наследия ЮНЕСКО.",
            short_description="Уникальные скалы-столбы высотой до 100 метров",
            image_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            icon="mountain",
            color="#10B981"
        ),
        GeographicPoint(
            name="Саяны",
            type="nature",
            latitude=52.0,
            longitude=93.5,
            description="Горная система на юге Сибири. Западный и Восточный Саян окружают верховья Енисея. Высочайшая вершина — пик Грандиозный (2922 м). Царство тайги, альпийских лугов, горных рек и водопадов. Место обитания редких животных: снежного барса, сибирского горного козла.",
            short_description="Величественная горная система верховий Енисея",
            image_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            icon="mountain",
            color="#059669"
        ),
        GeographicPoint(
            name="Плато Путорана",
            type="nature",
            latitude=69.0,
            longitude=93.0,
            description="Одно из самых диких и труднодоступных мест планеты. Базальтовые плато, глубокие каньоны, тысячи озер и водопадов. Объект ЮНЕСКО. Здесь обитает крупнейшая популяция диких северных оленей. Территория практически не тронута человеком.",
            short_description="Дикое плато с каньонами и водопадами",
            image_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            icon="mountain",
            color="#047857"
        ),
        
        # Исторические места
        GeographicPoint(
            name="Красноярская ГЭС",
            type="landmark",
            latitude=55.9622,
            longitude=92.3642,
            description="Одна из крупнейших гидроэлектростанций мира. Высота плотины — 124 метра, мощность — 6000 МВт. Символ индустриальной мощи. Изображена на 10-рублевой купюре. Экскурсии на смотровую площадку открывают панораму могучей плотины и Енисея.",
            short_description="Энергетический гигант на купюре 10 рублей",
            image_url="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e",
            icon="landmark",
            color="#8B5CF6"
        ),
        GeographicPoint(
            name="Шалаболинская писаница",
            type="historical",
            latitude=55.7,
            longitude=91.2,
            description="Комплекс древних наскальных рисунков возрастом до 5000 лет. Изображения животных, охотников, шаманов и солярных символов. Один из важнейших памятников наскального искусства Сибири. Расположен на правом берегу Енисея.",
            short_description="Древние петроглифы возрастом 5000 лет",
            image_url="https://images.unsplash.com/photo-1551847677-dc82d764e1eb",
            icon="landmark",
            color="#A855F7"
        )
    ]
    
    db.add_all(points)
    db.commit()
    print(f"✅ Добавлено {len(points)} географических точек")

def seed_gallery(db: Session):
    """Создать галерею изображений"""
    images = [
        GalleryImage(
            title="Енисей в Саянах",
            description="Живописный каньон Енисея в горах Саяны. Бирюзовая вода, отвесные скалы и девственная тайга.",
            image_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            category="nature",
            photographer="Виктор Козлов",
            year_taken=2022,
            location="Саяны, Тыва",
            order_index=1,
            is_featured=True
        ),
        GalleryImage(
            title="Закат на Енисее",
            description="Золотой закат окрашивает воды Енисея в багряные тона. Силуэты деревьев на берегу.",
            image_url="https://images.unsplash.com/photo-1469474968028-56623f02e42e",
            category="nature",
            photographer="Анна Петрова",
            year_taken=2021,
            location="Красноярское водохранилище",
            order_index=2,
            is_featured=True
        ),
        GalleryImage(
            title="Ледоход на Енисее",
            description="Мощный ледоход — величественное и опасное явление. Тысячи тонн льда движутся по реке.",
            image_url="https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5",
            category="nature",
            photographer="Сергей Иванов",
            year_taken=2023,
            location="Красноярск",
            order_index=3,
            is_featured=False
        ),
        GalleryImage(
            title="Красноярские Столбы",
            description="Знаменитые скалы-столбы — символ Красноярского края. Любимое место скалолазов и туристов.",
            image_url="https://images.unsplash.com/photo-1464207687429-7505649dae38",
            category="nature",
            photographer="Дмитрий Соколов",
            year_taken=2022,
            location="Национальный парк 'Столбы'",
            order_index=4,
            is_featured=True
        ),
        GalleryImage(
            title="Енисей зимой",
            description="Зимний Енисей в Красноярске. Река не замерзает благодаря сбросу теплой воды с ГЭС.",
            image_url="https://images.unsplash.com/photo-1491002052546-bf38f186af56",
            category="nature",
            photographer="Елена Морозова",
            year_taken=2020,
            location="Красноярск",
            order_index=5,
            is_featured=False
        ),
        GalleryImage(
            title="Коммунальный мост",
            description="Знаменитый вантовый мост через Енисей в Красноярске. Символ города на 10-рублевой купюре.",
            image_url="https://images.unsplash.com/photo-1519817914152-22d216bb9170",
            category="architecture",
            photographer="Александр Белов",
            year_taken=2021,
            location="Красноярск",
            order_index=6,
            is_featured=False
        ),
        GalleryImage(
            title="Северное сияние над Енисеем",
            description="Магическое северное сияние танцует над водами Енисея за Полярным кругом.",
            image_url="https://images.unsplash.com/photo-1531366936337-7c912a4589a7",
            category="nature",
            photographer="Николай Арктический",
            year_taken=2023,
            location="Дудинка",
            order_index=7,
            is_featured=True
        ),
        GalleryImage(
            title="Сибирская тайга",
            description="Бескрайняя тайга вдоль берегов Енисея. Одна из последних диких территорий планеты.",
            image_url="https://images.unsplash.com/photo-1448375240586-882707db888b",
            category="nature",
            photographer="Ольга Лесная",
            year_taken=2022,
            location="Енисейский район",
            order_index=8,
            is_featured=False
        )
    ]
    
    db.add_all(images)
    db.commit()
    print(f"✅ Добавлено {len(images)} изображений в галерею")

def seed_quiz_questions(db: Session):
    """Создать вопросы викторины"""
    questions = [
        # География и рекорды (1-10)
        QuizQuestion(
            question="Где берет начало Енисей?",
            option_a="Слияние Большого и Малого Енисея",
            option_b="Озеро Байкал",
            option_c="Ледники Алтая",
            option_d="Ледники Саян",
            correct_answer="A",
            explanation="Енисей образуется в результате слияния Большого и Малого Енисея в Туве. Это одна из величайших рек мира.",
            difficulty="easy",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="В какой океан впадает река?",
            option_a="Северный Ледовитый",
            option_b="Тихий",
            option_c="Атлантический",
            option_d="Индийский",
            correct_answer="A",
            explanation="Енисей впадает в Северный Ледовитый океан через Карское море. Это одна из величайших рек мира по полноводности.",
            difficulty="easy",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="Какое море принимает воды Енисея?",
            option_a="Карское",
            option_b="Лаптевых",
            option_c="Баренцево",
            option_d="Белое",
            correct_answer="A",
            explanation="Енисей впадает в Карское море, которое является частью Северного Ледовитого океана. Енисей выносит в океан около 600 куб. км пресной воды в год.",
            difficulty="easy",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="Какое место по длине занимает Енисей среди всех рек России?",
            option_a="1-е место",
            option_b="2-е место",
            option_c="3-е место",
            option_d="5-е место",
            correct_answer="B",
            explanation="Енисей занимает 2-е место по длине среди рек России после Оби. Его длина составляет 3487-4102 км в зависимости от выбора истока.",
            difficulty="medium",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="В каком городе находится обелиск «Центр Азии»?",
            option_a="Кызыл",
            option_b="Красноярск",
            option_c="Абакан",
            option_d="Минусинск",
            correct_answer="A",
            explanation="Обелиск «Центр Азии» находится в Кызыле — столице Республики Тыва, у истоков Енисея. Координаты: 51°43' северной широты и 104°58' восточной долготы.",
            difficulty="medium",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="Какая река является самым мощным притоком Енисея?",
            option_a="Ангара",
            option_b="Подкаменная Тунгуска",
            option_c="Кан",
            option_d="Туба",
            correct_answer="A",
            explanation="Ангара — самый мощный приток Енисея. Она преобразована каскадом ГЭС и является его крупнейшим притоком по полноводности.",
            difficulty="medium",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="Как называется залив, в который впадает Енисей?",
            option_a="Енисейский залив",
            option_b="Обская губа",
            option_c="Хатангский залив",
            option_d="Печорский залив",
            correct_answer="A",
            explanation="Енисей впадает в Енисейский залив — древний древний залив, образованный затоплением речной долины Енисея при подъеме уровня мирового океана.",
            difficulty="medium",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="Через сколько часовых поясов протекает Енисей?",
            option_a="1 пояс",
            option_b="3 пояса",
            option_c="5 поясов",
            option_d="7 поясов",
            correct_answer="A",
            explanation="Енисей протекает через 1 часовой пояс — Красноярское время (UTC+7). Это третий часовой пояс России.",
            difficulty="medium",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="Является ли Енисей природной границей между Западной и Восточной Сибирью?",
            option_a="Да",
            option_b="Нет",
            option_c="Только в нижнем течении",
            option_d="Только в верхнем течении",
            correct_answer="A",
            explanation="Да, Енисей служит природной и географической границей между Западной Сибирью (к западу) и Восточной Сибирью (к востоку).",
            difficulty="medium",
            category="geography",
            points=10
        ),
        QuizQuestion(
            question="Какое водохранилище на Енисее называют «Красноярским морем»?",
            option_a="Красноярское",
            option_b="Саяно-Шушенское",
            option_c="Майнское",
            option_d="Братское",
            correct_answer="A",
            explanation="Красноярское водохранилище (Красноярское море) образовано плотиной Красноярской ГЭС. Это одно из самых больших водохранилищ в России.",
            difficulty="easy",
            category="geography",
            points=10
        ),
        
        # История и освоение (11-20)
        QuizQuestion(
            question="Как переводится название «Ионесси» с древнетунгусского?",
            option_a="Большая вода",
            option_b="Быстрый поток",
            option_c="Холодное море",
            option_d="Сибирская река",
            correct_answer="A",
            explanation="«Ионесси» переводится с древнетунгусского как «Большая вода». Это название отражает величину и полноводность реки.",
            difficulty="hard",
            category="history",
            points=15
        ),
        QuizQuestion(
            question="В каком году был основан Енисейск, «отец городов сибирских»?",
            option_a="1619",
            option_b="1720",
            option_c="1147",
            option_d="1500",
            correct_answer="A",
            explanation="Енисейск был основан в 1619 году. Он считается первым русским городом в Восточной Сибири и началом освоения региона.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="Кто возглавил экспедицию, заложившую Красноярский острог?",
            option_a="Андрей Дубенский",
            option_b="Семен Дежнев",
            option_c="Ермак Тимофеевич",
            option_d="Василий Поярков",
            correct_answer="A",
            explanation="Воевода Андрей Дубенский в 1628 году основал Красноярский острог. Город с тех пор стал центром русского присутствия на Среднем Енисее.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="Как назывался первый пароход, появившийся на Енисее в 1863 году?",
            option_a="«Енисей»",
            option_b="«Сибирь»",
            option_c="«Николай»",
            option_d="«Амур»",
            correct_answer="A",
            explanation="Первый пароход, появившийся на Енисее в 1863 году, назывался «Енисей». Это был важный шаг в развитии транспорта в Сибири.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="Какое событие 1908 года произошло в бассейне притока Енисея?",
            option_a="Падение Тунгусского метеорита",
            option_b="Открытие золотых приисков",
            option_c="Первое зимнее плавание",
            option_d="Постройка железной дороги",
            correct_answer="A",
            explanation="В 1908 году в бассейне реки Подкаменная Тунгуска (притока Енисея) произошло падение Тунгусского метеорита — одного из самых мощных взрывов в истории.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="В каком городе находится знаменитый Музей вечной мерзлоты?",
            option_a="Игарка",
            option_b="Норильск",
            option_c="Дудинка",
            option_d="Хатанга",
            correct_answer="A",
            explanation="Музей вечной мерзлоты находится в Игарке — одном из самых северных портов на Енисее. Музей расположен в подземных туннелях вечной мерзлоты.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="Какое судно-музей навечно пришвартовано в Красноярске?",
            option_a="Пароход «Святитель Николай»",
            option_b="Крейсер «Аврора»",
            option_c="Ледокол «Арктика»",
            option_d="Корабль «Бигль»",
            correct_answer="A",
            explanation="Пароход «Святитель Николай» (построен в 1913 году) пришвартован в Красноярске и служит музеем истории навигации на Енисее.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="Для чего в XVII веке использовался Енисей в первую очередь?",
            option_a="Сбор ясака (пушнины)",
            option_b="Добыча нефти",
            option_c="Туризм",
            option_d="Гидроэнергетика",
            correct_answer="A",
            explanation="В XVII веке Енисей использовался в первую очередь для сбора ясака (пушнины) с местного населения. Пушной промысел был основой экономики региона.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="Как назывались традиционные деревянные лодки первопроходцев?",
            option_a="Кочи",
            option_b="Бриги",
            option_c="Фрегаты",
            option_d="Каноэ",
            correct_answer="A",
            explanation="Кочи — это традиционные деревянные лодки, использовавшиеся русскими первопроходцами для плавания по сибирским рекам. Они были приспособлены к ледовым условиям.",
            difficulty="medium",
            category="history",
            points=10
        ),
        QuizQuestion(
            question="Какой город на Енисее был крупнейшим центром золотодобычи в XIX веке?",
            option_a="Енисейск",
            option_b="Диксон",
            option_c="Саяногорск",
            option_d="Абакан",
            correct_answer="A",
            explanation="Енисейск был крупнейшим центром золотодобычи в XIX веке. Сюда стекались золотоискатели со всех концов России.",
            difficulty="medium",
            category="history",
            points=10
        ),
        
        # Природа и экология (21-30)
        QuizQuestion(
            question="Какая ценная рыба Енисея занесена в Красную книгу?",
            option_a="Сибирский осетр",
            option_b="Окунь",
            option_c="Карась",
            option_d="Плотва",
            correct_answer="A",
            explanation="Сибирский осетр (зубр) — ценная рыба, занесенная в Красную книгу России. Он может достигать размера до 3 метров и веса до 160 кг.",
            difficulty="easy",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Как называется знаменитый заповедник на правом берегу Енисея?",
            option_a="Столбы",
            option_b="Тайга",
            option_c="Саяны",
            option_d="Минусинские степи",
            correct_answer="A",
            explanation="Национальный парк «Красноярские Столбы» — уникальный заповедник на правом берегу Енисея с неповторимыми скальными образованиями высотой до 100 метров.",
            difficulty="easy",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Какое животное является символом приенисейской тайги?",
            option_a="Бурый медведь",
            option_b="Амурский тигр",
            option_c="Слон",
            option_d="Волк",
            correct_answer="A",
            explanation="Бурый медведь — символ приенисейской тайги и самый крупный хищник региона. Он обитает в лесах вдоль Енисея.",
            difficulty="medium",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Водятся ли в низовьях Енисея морские млекопитающие?",
            option_a="Да, белуха и нерпа",
            option_b="Нет, только речная рыба",
            option_c="Только дельфины",
            option_d="Никогда не водились",
            correct_answer="A",
            explanation="Да, в низовьях Енисея водятся белуха (белая китовая акула) и нерпа (арктический тюлень). Они заходят в устье и дельту реки.",
            difficulty="medium",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Какое дерево составляет основу «темнохвойной тайги» Енисея?",
            option_a="Кедр и пихта",
            option_b="Береза и осина",
            option_c="Ель и сосна",
            option_d="Лиственница",
            correct_answer="A",
            explanation="Кедр и пихта составляют основу темнохвойной тайги Енисея. Это высокопроизводительные и долгоживущие леса Сибири.",
            difficulty="medium",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Замерзает ли Енисей в черте Красноярска зимой?",
            option_a="Нет, из-за работы ГЭС",
            option_b="Да, лед очень толстый",
            option_c="Замерзает только в сильные морозы",
            option_d="Замерзает в верхней части, но не полностью",
            correct_answer="A",
            explanation="Нет, Енисей не замерзает в черте Красноярска из-за работы Красноярской ГЭС. Теплая вода с электростанции создает незамерзающую полынью.",
            difficulty="hard",
            category="ecology",
            points=15
        ),
        QuizQuestion(
            question="Какая птица прилетает в дельту Енисея на гнездование?",
            option_a="Краснозобая казарка",
            option_b="Попугай",
            option_c="Пингвин",
            option_d="Страус",
            correct_answer="A",
            explanation="Краснозобая казарка — редкая и исчезающая птица, которая прилетает в дельту Енисея на гнездование. Она занесена в Красную книгу.",
            difficulty="easy",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Какое уникальное природное явление можно наблюдать на севере Енисея?",
            option_a="Северное сияние",
            option_b="Песчаные бури",
            option_c="Гейзеры",
            option_d="Цунами",
            correct_answer="A",
            explanation="Северное сияние (полярное сияние) можно наблюдать на севере Енисея осенью и зимой благодаря высокой широте (более 70°).",
            difficulty="medium",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Как называется самый северный порт Енисея?",
            option_a="Диксон",
            option_b="Дудинка",
            option_c="Игарка",
            option_d="Норильск",
            correct_answer="A",
            explanation="Диксон — самый северный морской порт Енисея, расположенный на Полярном Урале. Это важнейший грузовой порт для снабжения российской Арктики.",
            difficulty="medium",
            category="ecology",
            points=10
        ),
        QuizQuestion(
            question="Какая ягода считается «царицей» енисейских болот?",
            option_a="Клюква",
            option_b="Клубника",
            option_c="Виноград",
            option_d="Черника",
            correct_answer="A",
            explanation="Клюква считается «царицей» енисейских болот. Это ценная ягода, богатая витаминами, растет на болотах вдоль Енисея.",
            difficulty="easy",
            category="ecology",
            points=10
        )
    ]
    
    db.add_all(questions)
    db.commit()
    print(f"✅ Добавлено {len(questions)} вопросов викторины")

def seed_interesting_facts(db: Session):
    """Создать интересные факты"""
    facts = [
        InterestingFact(
            title="Енисей — самая полноводная река России",
            fact="Енисей сбрасывает в Карское море около 600 км³ воды в год — больше, чем любая другая река России. Это примерно в 3 раза больше, чем Волга!",
            category="nature",
            icon="droplet",
            order_index=1
        ),
        InterestingFact(
            title="Граница Западной и Восточной Сибири",
            fact="Енисей служит условной границей между Западной Сибирью (к западу) и Восточной Сибирью (к востоку). Меняется даже ландшафт: на западе — равнины, на востоке — горы и возвышенности.",
            category="geography",
            icon="map",
            order_index=2
        ),
        InterestingFact(
            title="Енисей не замерзает в Красноярске",
            fact="Участок Енисея ниже Красноярской ГЭС не замерзает даже в 40-градусные морозы! Теплая вода с электростанции создает незамерзающую полынью протяженностью более 200 км.",
            category="nature",
            icon="snowflake",
            order_index=3
        ),
        InterestingFact(
            title="На дне Енисея лежит атомный реактор",
            fact="В 1967 году у поселка Атаманово в Енисей был сброшен отработавший ядерный реактор с ледокола. Он до сих пор лежит на дне под толщей ила и контролируется специалистами.",
            category="history",
            icon="alert-triangle",
            order_index=4
        ),
        InterestingFact(
            title="Енисей на 10-рублевой купюре",
            fact="Красноярская ГЭС и Коммунальный мост через Енисей изображены на российской купюре достоинством 10 рублей. Это единственная река, представленная на современных российских деньгах.",
            category="culture",
            icon="banknote",
            order_index=5
        ),
        InterestingFact(
            title="Самая северная река мира",
            fact="Енисей — самая северная из великих рек планеты. Его устье находится за 70° северной широты, в зоне вечной мерзлоты и тундры.",
            category="geography",
            icon="compass",
            order_index=6
        ),
        InterestingFact(
            title="Енисейский мост — чудо инженерии",
            fact="Железнодорожный мост через Енисей в Красноярске (построен в 1899 году) получил Гран-при на Всемирной выставке в Париже в 1900 году наравне с Эйфелевой башней!",
            category="history",
            icon="award",
            order_index=7
        ),
        InterestingFact(
            title="В Енисее водится 42 вида рыб",
            fact="В водах Енисея обитает 42 вида рыб, включая осетра, стерлядь, нельму, муксуна, тайменя. Некоторые виды занесены в Красную книгу.",
            category="ecology",
            icon="fish",
            order_index=8
        ),
        InterestingFact(
            title="Разница температур — 100 градусов!",
            fact="В верховьях Енисея летом вода прогревается до +20°C, а в устье даже летом редко теплее +8°C. Зимой разница температур воздуха от истока до устья может превышать 100 градусов!",
            category="nature",
            icon="thermometer",
            order_index=9
        ),
        InterestingFact(
            title="Енисей старше динозавров",
            fact="Возраст речной долины Енисея оценивается более чем в 50 миллионов лет. Река текла здесь еще до появления человека на Земле.",
            category="nature",
            icon="clock",
            order_index=10
        )
    ]
    
    db.add_all(facts)
    db.commit()
    print(f"✅ Добавлено {len(facts)} интересных фактов")

def main():
    """Главная функция для запуска заполнения БД"""
    print("=" * 50)
    print("🌊 ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ 'ИСТОРИЯ ЕНИСЕЯ' 🌊")
    print("=" * 50)
    
    # Очищаем базу
    clear_database()
    
    # Создаем сессию
    db = SessionLocal()
    
    try:
        # Заполняем данными
        print("\n📚 Создание эпох...")
        epochs = seed_epochs(db)
        
        print("\n📖 Создание исторических событий...")
        seed_historical_events(db, epochs)
        
        print("\n🗺️  Создание географических точек...")
        seed_geographic_points(db)
        
        print("\n🖼️  Создание галереи...")
        seed_gallery(db)
        
        print("\n❓ Создание вопросов викторины...")
        seed_quiz_questions(db)
        
        print("\n💡 Создание интересных фактов...")
        seed_interesting_facts(db)
        
        print("\n" + "=" * 50)
        print("✅ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
        print("=" * 50)
        print(f"\n📊 Статистика:")
        print(f"   • Эпох: {db.query(Epoch).count()}")
        print(f"   • Событий: {db.query(HistoricalEvent).count()}")
        print(f"   • Географических точек: {db.query(GeographicPoint).count()}")
        print(f"   • Изображений: {db.query(GalleryImage).count()}")
        print(f"   • Вопросов: {db.query(QuizQuestion).count()}")
        print(f"   • Фактов: {db.query(InterestingFact).count()}")
        print("\n🚀 Запустите сервер: python main.py")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()