from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random
import re

app = FastAPI(title="Food AI Assistant API")

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class FoodItem(BaseModel):
    name: str
    calories: int
    protein: float
    carbs: float
    fats: float
    category: str
    description: str
    recipe: str
    tags: List[str] = []

class FoodRequest(BaseModel):
    query: str
    user_calories: Optional[int] = 2000
    preferences: List[str] = []

# РАСШИРЕННАЯ БАЗА ДАННЫХ (50+ БЛЮД)
FOOD_DATABASE = [
    # ЗАВТРАКИ (10 блюд)
    FoodItem(
        name="Овсяная каша с ягодами и орехами",
        calories=320,
        protein=12.5,
        carbs=52.0,
        fats=8.5,
        category="завтрак",
        description="Питательный завтрак с высоким содержанием клетчатки",
        recipe="50г овсянки, 200мл молока, горсть ягод, 20г орехов, мед",
        tags=["здоровый", "вегетарианский", "быстрый"]
    ),
    FoodItem(
        name="Омлет с овощами и сыром",
        calories=280,
        protein=22.0,
        carbs=8.0,
        fats=18.0,
        category="завтрак",
        description="Белковый завтрак с витаминами",
        recipe="3 яйца, помидор, болгарский перец, 30г сыра, зелень",
        tags=["белковый", "быстрый", "сытный"]
    ),
    FoodItem(
        name="Творожная запеканка",
        calories=250,
        protein=20.0,
        carbs=25.0,
        fats=8.0,
        category="завтрак",
        description="Нежный творожный завтрак",
        recipe="200г творога, 1 яйцо, 2 ст.л. манки, изюм, ванилин",
        tags=["творог", "сладкий", "детский"]
    ),
    FoodItem(
        name="Гречневая каша с молоком",
        calories=300,
        protein=10.5,
        carbs=55.0,
        fats=6.0,
        category="завтрак",
        description="Традиционный русский завтрак",
        recipe="70г гречки, 200мл молока, сливочное масло, сахар",
        tags=["традиционный", "простой", "дешевый"]
    ),
    FoodItem(
        name="Смузи-боул с фруктами",
        calories=270,
        protein=8.0,
        carbs=45.0,
        fats=7.0,
        category="завтрак",
        description="Свежий и витаминный завтрак",
        recipe="Банан, киви, ягоды, йогурт, мюсли, семена чиа",
        tags=["фруктовый", "витаминный", "летний"]
    ),
    FoodItem(
        name="Блины с творогом",
        calories=350,
        protein=15.0,
        carbs=45.0,
        fats=12.0,
        category="завтрак",
        description="Вкусный воскресный завтрак",
        recipe="Блины: мука, молоко, яйца. Начинка: творог, сметана",
        tags=["традиционный", "праздничный", "сладкий"]
    ),
    FoodItem(
        name="Яичница с авокадо",
        calories=320,
        protein=16.0,
        carbs=10.0,
        fats=25.0,
        category="завтрак",
        description="Здоровые жиры и белок",
        recipe="2 яйца, 1/2 авокадо, помидор, цельнозерновой хлеб",
        tags=["пп", "здоровый", "быстрый"]
    ),
    FoodItem(
        name="Сырники с джемом",
        calories=280,
        protein=18.0,
        carbs=30.0,
        fats=10.0,
        category="завтрак",
        description="Любимый завтрак детей и взрослых",
        recipe="Творог, яйцо, мука, сахар. Жарить на антипригарной сковороде",
        tags=["творог", "сладкий", "детский"]
    ),
    FoodItem(
        name="Французские тосты",
        calories=310,
        protein=12.0,
        carbs=40.0,
        fats=11.0,
        category="завтрак",
        description="Сладкий хрустящий завтрак",
        recipe="Хлеб, яйца, молоко, корица, мед. Обжарить с двух сторон",
        tags=["сладкий", "быстрый", "десерт"]
    ),
    FoodItem(
        name="Гранола с йогуртом",
        calories=290,
        protein=9.0,
        carbs=42.0,
        fats=9.0,
        category="завтрак",
        description="Хрустящий и полезный завтрак",
        recipe="Домашняя гранола, греческий йогурт, свежие фрукты",
        tags=["хрустящий", "здоровый", "быстрый"]
    ),
    
    # ОБЕДЫ (15 блюд)
    FoodItem(
        name="Куриная грудка с киноа и овощами",
        calories=420,
        protein=45.0,
        carbs=35.0,
        fats=12.0,
        category="обед",
        description="Высокобелковый обед для мышц",
        recipe="200г куриной грудки, 100г киноа, брокколи, морковь, специи",
        tags=["белковый", "пп", "после тренировки"]
    ),
    FoodItem(
        name="Лосось на гриле с булгуром",
        calories=450,
        protein=35.0,
        carbs=40.0,
        fats=18.0,
        category="обед",
        description="Богат омега-3 жирными кислотами",
        recipe="200г лосося, 80г булгура, спаржа, лимон, укроп",
        tags=["рыба", "праздничный", "здоровый"]
    ),
    FoodItem(
        name="Говядина с гречкой",
        calories=480,
        protein=38.0,
        carbs=45.0,
        fats=16.0,
        category="обед",
        description="Источник железа и белка",
        recipe="150г говядины, 100г гречки, лук, морковь, томатная паста",
        tags=["мясо", "сытный", "традиционный"]
    ),
    FoodItem(
        name="Индейка с картофелем",
        calories=400,
        protein=35.0,
        carbs=38.0,
        fats=12.0,
        category="обед",
        description="Диетическое мясо с гарниром",
        recipe="180г индейки, 150г картофеля, цветная капуста, розмарин",
        tags=["диетический", "мясо", "семейный"]
    ),
    FoodItem(
        name="Суп-пюре из тыквы",
        calories=320,
        protein=8.0,
        carbs=40.0,
        fats=15.0,
        category="обед",
        description="Нежный и сытный суп",
        recipe="Тыква, картофель, лук, сливки, имбирь, семечки тыквенные",
        tags=["суп", "вегетарианский", "осенний"]
    ),
    FoodItem(
        name="Паста с морепродуктами",
        calories=430,
        protein=25.0,
        carbs=55.0,
        fats=12.0,
        category="обед",
        description="Итальянская классика",
        recipe="Макароны из твердых сортов, креветки, мидии, чеснок, вино",
        tags=["итальянский", "морепродукты", "праздничный"]
    ),
    FoodItem(
        name="Фаршированные перцы",
        calories=350,
        protein=20.0,
        carbs=30.0,
        fats=15.0,
        category="обед",
        description="Домашняя еда как у бабушки",
        recipe="Болгарские перцы, фарш, рис, лук, морковь, томатный соус",
        tags=["домашний", "традиционный", "семейный"]
    ),
    FoodItem(
        name="Котлеты из индейки с пюре",
        calories=380,
        protein=28.0,
        carbs=35.0,
        fats=14.0,
        category="обед",
        description="Нежные котлеты с гарниром",
        recipe="Фарш индейки, лук, картофельное пюре, зеленый горошек",
        tags=["мясо", "домашний", "детский"]
    ),
    FoodItem(
        name="Рататуй",
        calories=280,
        protein=6.0,
        carbs=25.0,
        fats=16.0,
        category="обед",
        description="Овощное рагу по-провансальски",
        recipe="Баклажаны, кабачки, помидоры, перец, чеснок, базилик",
        tags=["вегетарианский", "французский", "овощи"]
    ),
    FoodItem(
        name="Плов с курицей",
        calories=460,
        protein=30.0,
        carbs=55.0,
        fats=14.0,
        category="обед",
        description="Сытное восточное блюдо",
        recipe="Рис, курица, морковь, лук, специи для плова, барбарис",
        tags=["восточный", "сытный", "праздничный"]
    ),
    FoodItem(
        name="Фахитос с курицей",
        calories=390,
        protein=32.0,
        carbs=30.0,
        fats=16.0,
        category="обед",
        description="Мексиканская кухня",
        recipe="Курица, болгарский перец, лук, тортильи, гуакамоле, сметана",
        tags=["мексиканский", "острое", "тортильи"]
    ),
    FoodItem(
        name="Стейк из тунца с салатом",
        calories=320,
        protein=40.0,
        carbs=8.0,
        fats=14.0,
        category="обед",
        description="Рыбный стейк для гурманов",
        recipe="Стейк тунца, микс салатов, помидоры черри, соус цезарь",
        tags=["рыба", "ресторанный", "легкий"]
    ),
    FoodItem(
        name="Чечевичный суп",
        calories=310,
        protein=18.0,
        carbs=45.0,
        fats=6.0,
        category="обед",
        description="Богат белком и клетчаткой",
        recipe="Красная чечевица, морковь, лук, сельдерей, томаты, специи",
        tags=["суп", "вегетарианский", "белковый"]
    ),
    FoodItem(
        name="Запеченная курица с овощами",
        calories=380,
        protein=35.0,
        carbs=20.0,
        fats=18.0,
        category="обед",
        description="Простое и полезное блюдо",
        recipe="Куриные бедра, картофель, морковь, лук, прованские травы",
        tags=["простой", "семейный", "духовка"]
    ),
    FoodItem(
        name="Голубцы",
        calories=340,
        protein=22.0,
        carbs=30.0,
        fats=14.0,
        category="обед",
        description="Традиционное славянское блюдо",
        recipe="Капустные листья, фарш, рис, морковь, лук, томатная паста",
        tags=["традиционный", "славянский", "домашний"]
    ),
    
    # УЖИНЫ (10 блюд)
    FoodItem(
        name="Салат Цезарь с курицей",
        calories=320,
        protein=28.0,
        carbs=15.0,
        fats=16.0,
        category="ужин",
        description="Классический салат",
        recipe="Курица, салат романо, сухарики, пармезан, соус цезарь",
        tags=["салат", "классика", "быстрый"]
    ),
    FoodItem(
        name="Теплый салат с креветками",
        calories=280,
        protein=25.0,
        carbs=12.0,
        fats=14.0,
        category="ужин",
        description="Легкий ужин с морепродуктами",
        recipe="Креветки, авокадо, помидоры черри, руккола, оливковое масло",
        tags=["морепродукты", "легкий", "ресторанный"]
    ),
    FoodItem(
        name="Запеченные овощи с фетой",
        calories=250,
        protein=10.0,
        carbs=20.0,
        fats=15.0,
        category="ужин",
        description="Вегетарианский ужин",
        recipe="Кабачки, баклажаны, помидоры, сыр фета, оливковое масло",
        tags=["вегетарианский", "овощи", "греческий"]
    ),
    FoodItem(
        name="Тыквенный крем-суп",
        calories=220,
        protein=6.0,
        carbs=25.0,
        fats=10.0,
        category="ужин",
        description="Легкий и согревающий",
        recipe="Тыква, лук, имбирь, кокосовое молоко, тыквенные семечки",
        tags=["суп", "вегетарианский", "осенний"]
    ),
    FoodItem(
        name="Куриные шашлычки",
        calories=290,
        protein=30.0,
        carbs=8.0,
        fats=14.0,
        category="ужин",
        description="Диетический вариант шашлыка",
        recipe="Куриное филе, болгарский перец, лук, йогуртовый маринад",
        tags=["гриль", "летний", "шашлык"]
    ),
    FoodItem(
        name="Спаржа на гриле с яйцом пашот",
        calories=240,
        protein=18.0,
        carbs=10.0,
        fats=15.0,
        category="ужин",
        description="Изысканный ужин",
        recipe="Спаржа, яйцо пашот, пармезан, трюфельное масло",
        tags=["изысканный", "ресторанный", "легкий"]
    ),
    FoodItem(
        name="Греческий салат",
        calories=260,
        protein=8.0,
        carbs=12.0,
        fats=20.0,
        category="ужин",
        description="Свежий средиземноморский салат",
        recipe="Помидоры, огурцы, перец, оливки, сыр фета, оливковое масло",
        tags=["салат", "греческий", "летний"]
    ),
    FoodItem(
        name="Фаршированные кабачки",
        calories=230,
        protein=12.0,
        carbs=15.0,
        fats=14.0,
        category="ужин",
        description="Низкокалорийный ужин",
        recipe="Кабачки, фарш куриный, лук, помидоры, сыр, зелень",
        tags=["овощи", "диетический", "домашний"]
    ),
    FoodItem(
        name="Суп том-ям",
        calories=210,
        protein=15.0,
        carbs=12.0,
        fats=10.0,
        category="ужин",
        description="Острый тайский суп",
        recipe="Креветки, грибы, лемонграсс, галангал, кокосовое молоко",
        tags=["тайский", "острый", "экзотический"]
    ),
    FoodItem(
        name="Овощное рагу",
        calories=200,
        protein=7.0,
        carbs=25.0,
        fats=8.0,
        category="ужин",
        description="Легкое овощное блюдо",
        recipe="Капуста, морковь, лук, кабачки, помидоры, зелень",
        tags=["овощи", "простой", "дешевый"]
    ),
    
    # ПЕРЕКУСЫ (10 блюд)
    FoodItem(
        name="Греческий йогурт с фруктами",
        calories=180,
        protein=12.0,
        carbs=20.0,
        fats=5.0,
        category="перекус",
        description="Белковый перекус",
        recipe="150г греческого йогурта, ягоды, мед, миндаль",
        tags=["йогурт", "сладкий", "быстрый"]
    ),
    FoodItem(
        name="Протеиновый коктейль",
        calories=220,
        protein=25.0,
        carbs=20.0,
        fats=4.0,
        category="перекус",
        description="Идеально после тренировки",
        recipe="Протеин, банан, молоко, арахисовая паста",
        tags=["протеин", "после тренировки", "спорт"]
    ),
    FoodItem(
        name="Ореховая смесь",
        calories=200,
        protein=8.0,
        carbs=10.0,
        fats=16.0,
        category="перекус",
        description="Энергетический перекус",
        recipe="Миндаль, грецкие орехи, кешью, сушеная клюква",
        tags=["орехи", "энергия", "быстрый"]
    ),
    FoodItem(
        name="Яблоко с арахисовой пастой",
        calories=190,
        protein=5.0,
        carbs=25.0,
        fats=9.0,
        category="перекус",
        description="Сладкий и полезный перекус",
        recipe="1 яблоко, 1 ст.л. арахисовой пасты",
        tags=["фрукты", "сладкий", "простой"]
    ),
    FoodItem(
        name="Творог с ягодами",
        calories=210,
        protein=22.0,
        carbs=15.0,
        fats=7.0,
        category="перекус",
        description="Классический белковый перекус",
        recipe="200г творога, горсть ягод, 1 ч.л. меда",
        tags=["творог", "белковый", "пп"]
    ),
    FoodItem(
        name="Смузи из шпината",
        calories=150,
        protein=6.0,
        carbs=25.0,
        fats=3.0,
        category="перекус",
        description="Витаминный коктейль",
        recipe="Шпинат, банан, яблоко, имбирь, вода",
        tags=["смузи", "витамины", "детокс"]
    ),
    FoodItem(
        name="Роллы из индейки",
        calories=170,
        protein=20.0,
        carbs=5.0,
        fats=8.0,
        category="перекус",
        description="Белковые рулетики",
        recipe="Ломтики индейки, творожный сыр, огурцы, листья салата",
        tags=["мясо", "белковый", "быстрый"]
    ),
    FoodItem(
        name="Запеченные яблоки",
        calories=160,
        protein=2.0,
        carbs=35.0,
        fats=3.0,
        category="перекус",
        description="Теплый десерт",
        recipe="Яблоки, корица, мед, грецкие орехи",
        tags=["десерт", "фрукты", "теплый"]
    ),
    FoodItem(
        name="Рыбные палочки",
        calories=230,
        protein=18.0,
        carbs=15.0,
        fats=10.0,
        category="перекус",
        description="Быстрая закуска",
        recipe="Филе белой рыбы, панировка, запекать в духовке",
        tags=["рыба", "быстрый", "детский"]
    ),
    FoodItem(
        name="Кексы из нута",
        calories=200,
        protein=10.0,
        carbs=25.0,
        fats=7.0,
        category="перекус",
        description="Полезная выпечка",
        recipe="Нутовая мука, яйца, банан, разрыхлитель, орехи",
        tags=["выпечка", "полезная", "вегетарианский"]
    ),
    
    # ВЕГЕТАРИАНСКИЕ (5 блюд)
    FoodItem(
        name="Фалафель с хумусом",
        calories=340,
        protein=15.0,
        carbs=40.0,
        fats=12.0,
        category="вегетарианский",
        description="Ближневосточная кухня",
        recipe="Нут, кунжутная паста, специи, питы, овощи",
        tags=["вегетарианский", "восточный", "нут"]
    ),
    FoodItem(
        name="Чечевичные котлеты",
        calories=290,
        protein=18.0,
        carbs=35.0,
        fats=8.0,
        category="вегетарианский",
        description="Богаты белком",
        recipe="Красная чечевица, лук, морковь, овсяные хлопья, специи",
        tags=["вегетарианский", "белковый", "котлеты"]
    ),
    FoodItem(
        name="Тофу с овощами вок",
        calories=280,
        protein=20.0,
        carbs=15.0,
        fats=16.0,
        category="вегетарианский",
        description="Азиатское блюдо",
        recipe="Тофу, болгарский перец, морковь, брокколи, соевый соус",
        tags=["вегетарианский", "азиатский", "тофу"]
    ),
    FoodItem(
        name="Грибной жюльен",
        calories=260,
        protein=10.0,
        carbs=12.0,
        fats=18.0,
        category="вегетарианский",
        description="Нежная закуска",
        recipe="Шампиньоны, лук, сметана, сыр, запекать в кокотницах",
        tags=["грибы", "закуска", "праздничный"]
    ),
    FoodItem(
        name="Спагетти с песто",
        calories=380,
        protein=12.0,
        carbs=50.0,
        fats=15.0,
        category="вегетарианский",
        description="Итальянская паста",
        recipe="Спагетти, соус песто, помидоры черри, пармезан, кедровые орехи",
        tags=["паста", "итальянский", "вегетарианский"]
    )
]

# Ключевые слова для определения категории
CATEGORY_KEYWORDS = {
    "завтрак": ["завтрак", "утро", "утром", "кофе", "каша", "омлет", "тост", "хлопья"],
    "обед": ["обед", "днем", "полдник", "суп", "горячее", "первое", "второе"],
    "ужин": ["ужин", "вечер", "ночь", "легкий", "салат"],
    "перекус": ["перекус", "снек", "фрукт", "йогурт", "творог", "орехи"],
    "вегетарианский": ["вегетарианский", "без мяса", "постный", "овощи"]
}

@app.get("/")
def read_root():
    return {"message": "Food AI Assistant API работает!"}

@app.post("/api/recommend")
def recommend_food(request: FoodRequest):
    """Основная функция рекомендаций на основе текстового запроса"""
    query = request.query.lower()
    
    # 1. Определяем категорию из запроса
    detected_category = "обед"  # по умолчанию
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in query for keyword in keywords):
            detected_category = category
            break
    
    # 2. Пытаемся найти числовое значение калорий в запросе
    numbers = re.findall(r'\d+', query)
    target_calories = request.user_calories / 3  # по умолчанию (3 приема пищи)
    
    if numbers:
        # Если пользователь указал калории, используем их
        user_target = int(numbers[0])
        # Проверяем, реалистично ли число (не больше 1000 для одного приема)
        if user_target < 1000:
            target_calories = user_target
        else:
            target_calories = user_target / 3
    
    # 3. Фильтруем блюда по категории
    filtered_foods = [f for f in FOOD_DATABASE if f.category == detected_category]
    
    # 4. Сортируем по близости к целевым калориям
    sorted_foods = sorted(filtered_foods, key=lambda f: abs(f.calories - target_calories))
    
    # 5. Берем лучшее блюдо
    recommendation = sorted_foods[0] if sorted_foods else random.choice(FOOD_DATABASE)
    
    # 6. Добавляем анализ запроса в ответ
    analysis = {
        "original_query": request.query,
        "detected_category": detected_category,
        "target_calories": round(target_calories, 0),
        "total_matches": len(sorted_foods)
    }
    
    return {
        "recommendation": recommendation,
        "analysis": analysis,
        "alternatives": sorted_foods[1:4]  # топ-3 альтернативы
    }

@app.get("/api/foods/all")
def get_all_foods(category: str = None):
    """Получить все блюда (с фильтром по категории)"""
    if category:
        filtered = [f for f in FOOD_DATABASE if f.category == category]
        return {"count": len(filtered), "foods": filtered}
    return {"count": len(FOOD_DATABASE), "foods": FOOD_DATABASE}

@app.get("/api/foods/categories")
def get_categories():
    """Получить все категории"""
    categories = list(set(f.category for f in FOOD_DATABASE))
    return {"categories": categories}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)