from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="Food AI Assistant API")

# Разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class FoodRequest(BaseModel):
    query: str
    user_calories: Optional[int] = 2000
    preferences: List[str] = []

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

# База данных в памяти
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
        recipe="50г овсянки, 200мл молока, горсть ягод, 20г орехов, мед"
    ),
    FoodItem(
        name="Омлет с овощами и сыром",
        calories=280,
        protein=22.0,
        carbs=8.0,
        fats=18.0,
        category="завтрак",
        description="Белковый завтрак с витаминами",
        recipe="3 яйца, помидор, болгарский перец, 30г сыра, зелень"
    ),
    FoodItem(
        name="Творожная запеканка",
        calories=250,
        protein=20.0,
        carbs=25.0,
        fats=8.0,
        category="завтрак",
        description="Нежный творожный завтрак",
        recipe="200г творога, 1 яйцо, 2 ст.л. манки, изюм, ванилин"
    ),
    FoodItem(
        name="Гречневая каша с молоком",
        calories=300,
        protein=10.5,
        carbs=55.0,
        fats=6.0,
        category="завтрак",
        description="Традиционный русский завтрак",
        recipe="70г гречки, 200мл молока, сливочное масло, сахар"
    ),
    FoodItem(
        name="Смузи-боул с фруктами",
        calories=270,
        protein=8.0,
        carbs=45.0,
        fats=7.0,
        category="завтрак",
        description="Свежий и витаминный завтрак",
        recipe="Банан, киви, ягоды, йогурт, мюсли, семена чиа"
    ),
    FoodItem(
        name="Блины с творогом",
        calories=350,
        protein=15.0,
        carbs=45.0,
        fats=12.0,
        category="завтрак",
        description="Вкусный воскресный завтрак",
        recipe="Блины: мука, молоко, яйца. Начинка: творог, сметана"
    ),
    FoodItem(
        name="Яичница с авокадо",
        calories=320,
        protein=16.0,
        carbs=10.0,
        fats=25.0,
        category="завтрак",
        description="Здоровые жиры и белок",
        recipe="2 яйца, 1/2 авокадо, помидор, цельнозерновой хлеб"
    ),
    FoodItem(
        name="Сырники с джемом",
        calories=280,
        protein=18.0,
        carbs=30.0,
        fats=10.0,
        category="завтрак",
        description="Любимый завтрак детей и взрослых",
        recipe="Творог, яйцо, мука, сахар. Жарить на антипригарной сковороде"
    ),
    FoodItem(
        name="Французские тосты",
        calories=310,
        protein=12.0,
        carbs=40.0,
        fats=11.0,
        category="завтрак",
        description="Сладкий хрустящий завтрак",
        recipe="Хлеб, яйца, молоко, корица, мед. Обжарить с двух сторон"
    ),
    FoodItem(
        name="Гранола с йогуртом",
        calories=290,
        protein=9.0,
        carbs=42.0,
        fats=9.0,
        category="завтрак",
        description="Хрустящий и полезный завтрак",
        recipe="Домашняя гранола, греческий йогурт, свежие фрукты"
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
        recipe="200г куриной грудки, 100г киноа, брокколи, морковь, специи"
    ),
    FoodItem(
        name="Лосось на гриле с булгуром",
        calories=450,
        protein=35.0,
        carbs=40.0,
        fats=18.0,
        category="обед",
        description="Богат омега-3 жирными кислотами",
        recipe="200г лосося, 80г булгура, спаржа, лимон, укроп"
    ),
    FoodItem(
        name="Говядина с гречкой",
        calories=480,
        protein=38.0,
        carbs=45.0,
        fats=16.0,
        category="обед",
        description="Источник железа и белка",
        recipe="150г говядины, 100г гречки, лук, морковь, томатная паста"
    ),
    FoodItem(
        name="Индейка с картофелем",
        calories=400,
        protein=35.0,
        carbs=38.0,
        fats=12.0,
        category="обед",
        description="Диетическое мясо с гарниром",
        recipe="180г индейки, 150г картофеля, цветная капуста, розмарин"
    ),
    FoodItem(
        name="Суп-пюре из тыквы",
        calories=320,
        protein=8.0,
        carbs=40.0,
        fats=15.0,
        category="обед",
        description="Нежный и сытный суп",
        recipe="Тыква, картофель, лук, сливки, имбирь, семечки тыквенные"
    ),
    FoodItem(
        name="Паста с морепродуктами",
        calories=430,
        protein=25.0,
        carbs=55.0,
        fats=12.0,
        category="обед",
        description="Итальянская классика",
        recipe="Макароны из твердых сортов, креветки, мидии, чеснок, вино"
    ),
    FoodItem(
        name="Фаршированные перцы",
        calories=350,
        protein=20.0,
        carbs=30.0,
        fats=15.0,
        category="обед",
        description="Домашняя еда как у бабушки",
        recipe="Болгарские перцы, фарш, рис, лук, морковь, томатный соус"
    ),
    FoodItem(
        name="Котлеты из индейки с пюре",
        calories=380,
        protein=28.0,
        carbs=35.0,
        fats=14.0,
        category="обед",
        description="Нежные котлеты с гарниром",
        recipe="Фарш индейки, лук, картофельное пюре, зеленый горошек"
    ),
    FoodItem(
        name="Рататуй",
        calories=280,
        protein=6.0,
        carbs=25.0,
        fats=16.0,
        category="обед",
        description="Овощное рагу по-провансальски",
        recipe="Баклажаны, кабачки, помидоры, перец, чеснок, базилик"
    ),
    FoodItem(
        name="Плов с курицей",
        calories=460,
        protein=30.0,
        carbs=55.0,
        fats=14.0,
        category="обед",
        description="Сытное восточное блюдо",
        recipe="Рис, курица, морковь, лук, специи для плова, барбарис"
    ),
    FoodItem(
        name="Фахитос с курицей",
        calories=390,
        protein=32.0,
        carbs=30.0,
        fats=16.0,
        category="обед",
        description="Мексиканская кухня",
        recipe="Курица, болгарский перец, лук, тортильи, гуакамоле, сметана"
    ),
    FoodItem(
        name="Стейк из тунца с салатом",
        calories=320,
        protein=40.0,
        carbs=8.0,
        fats=14.0,
        category="обед",
        description="Рыбный стейк для гурманов",
        recipe="Стейк тунца, микс салатов, помидоры черри, соус цезарь"
    ),
    FoodItem(
        name="Чечевичный суп",
        calories=310,
        protein=18.0,
        carbs=45.0,
        fats=6.0,
        category="обед",
        description="Богат белком и клетчаткой",
        recipe="Красная чечевица, морковь, лук, сельдерей, томаты, специи"
    ),
    FoodItem(
        name="Запеченная курица с овощами",
        calories=380,
        protein=35.0,
        carbs=20.0,
        fats=18.0,
        category="обед",
        description="Простое и полезное блюдо",
        recipe="Куриные бедра, картофель, морковь, лук, прованские травы"
    ),
    FoodItem(
        name="Голубцы",
        calories=340,
        protein=22.0,
        carbs=30.0,
        fats=14.0,
        category="обед",
        description="Традиционное славянское блюдо",
        recipe="Капустные листья, фарш, рис, морковь, лук, томатная паста"
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
        recipe="Курица, салат романо, сухарики, пармезан, соус цезарь"
    ),
    FoodItem(
        name="Теплый салат с креветками",
        calories=280,
        protein=25.0,
        carbs=12.0,
        fats=14.0,
        category="ужин",
        description="Легкий ужин с морепродуктами",
        recipe="Креветки, авокадо, помидоры черри, руккола, оливковое масло"
    ),
    FoodItem(
        name="Запеченные овощи с фетой",
        calories=250,
        protein=10.0,
        carbs=20.0,
        fats=15.0,
        category="ужин",
        description="Вегетарианский ужин",
        recipe="Кабачки, баклажаны, помидоры, сыр фета, оливковое масло"
    ),
    FoodItem(
        name="Тыквенный крем-суп",
        calories=220,
        protein=6.0,
        carbs=25.0,
        fats=10.0,
        category="ужин",
        description="Легкий и согревающий",
        recipe="Тыква, лук, имбирь, кокосовое молоко, тыквенные семечки"
    ),
    FoodItem(
        name="Куриные шашлычки",
        calories=290,
        protein=30.0,
        carbs=8.0,
        fats=14.0,
        category="ужин",
        description="Диетический вариант шашлыка",
        recipe="Куриное филе, болгарский перец, лук, йогуртовый маринад"
    ),
    FoodItem(
        name="Спаржа на гриле с яйцом пашот",
        calories=240,
        protein=18.0,
        carbs=10.0,
        fats=15.0,
        category="ужин",
        description="Изысканный ужин",
        recipe="Спаржа, яйцо пашот, пармезан, трюфельное масло"
    ),
    FoodItem(
        name="Греческий салат",
        calories=260,
        protein=8.0,
        carbs=12.0,
        fats=20.0,
        category="ужин",
        description="Свежий средиземноморский салат",
        recipe="Помидоры, огурцы, перец, оливки, сыр фета, оливковое масло"
    ),
    FoodItem(
        name="Фаршированные кабачки",
        calories=230,
        protein=12.0,
        carbs=15.0,
        fats=14.0,
        category="ужин",
        description="Низкокалорийный ужин",
        recipe="Кабачки, фарш куриный, лук, помидоры, сыр, зелень"
    ),
    FoodItem(
        name="Суп том-ям",
        calories=210,
        protein=15.0,
        carbs=12.0,
        fats=10.0,
        category="ужин",
        description="Острый тайский суп",
        recipe="Креветки, грибы, лемонграсс, галангал, кокосовое молоко"
    ),
    FoodItem(
        name="Овощное рагу",
        calories=200,
        protein=7.0,
        carbs=25.0,
        fats=8.0,
        category="ужин",
        description="Легкое овощное блюдо",
        recipe="Капуста, морковь, лук, кабачки, помидоры, зелень"
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
        recipe="150г греческого йогурта, ягоды, мед, миндаль"
    ),
    FoodItem(
        name="Протеиновый коктейль",
        calories=220,
        protein=25.0,
        carbs=20.0,
        fats=4.0,
        category="перекус",
        description="Идеально после тренировки",
        recipe="Протеин, банан, молоко, арахисовая паста"
    ),
    FoodItem(
        name="Ореховая смесь",
        calories=200,
        protein=8.0,
        carbs=10.0,
        fats=16.0,
        category="перекус",
        description="Энергетический перекус",
        recipe="Миндаль, грецкие орехи, кешью, сушеная клюква"
    ),
    FoodItem(
        name="Яблоко с арахисовой пастой",
        calories=190,
        protein=5.0,
        carbs=25.0,
        fats=9.0,
        category="перекус",
        description="Сладкий и полезный перекус",
        recipe="1 яблоко, 1 ст.л. арахисовой пасты"
    ),
    FoodItem(
        name="Творог с ягодами",
        calories=210,
        protein=22.0,
        carbs=15.0,
        fats=7.0,
        category="перекус",
        description="Классический белковый перекус",
        recipe="200г творога, горсть ягод, 1 ч.л. меда"
    ),
    FoodItem(
        name="Смузи из шпината",
        calories=150,
        protein=6.0,
        carbs=25.0,
        fats=3.0,
        category="перекус",
        description="Витаминный коктейль",
        recipe="Шпинат, банан, яблоко, имбирь, вода"
    ),
    FoodItem(
        name="Роллы из индейки",
        calories=170,
        protein=20.0,
        carbs=5.0,
        fats=8.0,
        category="перекус",
        description="Белковые рулетики",
        recipe="Ломтики индейки, творожный сыр, огурцы, листья салата"
    ),
    FoodItem(
        name="Запеченные яблоки",
        calories=160,
        protein=2.0,
        carbs=35.0,
        fats=3.0,
        category="перекус",
        description="Теплый десерт",
        recipe="Яблоки, корица, мед, грецкие орехи"
    ),
    FoodItem(
        name="Рыбные палочки",
        calories=230,
        protein=18.0,
        carbs=15.0,
        fats=10.0,
        category="перекус",
        description="Быстрая закуска",
        recipe="Филе белой рыбы, панировка, запекать в духовке"
    ),
    FoodItem(
        name="Кексы из нута",
        calories=200,
        protein=10.0,
        carbs=25.0,
        fats=7.0,
        category="перекус",
        description="Полезная выпечка",
        recipe="Нутовая мука, яйца, банан, разрыхлитель, орехи"
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
        recipe="Нут, кунжутная паста, специи, питы, овощи"
    ),
    FoodItem(
        name="Чечевичные котлеты",
        calories=290,
        protein=18.0,
        carbs=35.0,
        fats=8.0,
        category="вегетарианский",
        description="Богаты белком",
        recipe="Красная чечевица, лук, морковь, овсяные хлопья, специи"
    ),
    FoodItem(
        name="Тофу с овощами вок",
        calories=280,
        protein=20.0,
        carbs=15.0,
        fats=16.0,
        category="вегетарианский",
        description="Азиатское блюдо",
        recipe="Тофу, болгарский перец, морковь, брокколи, соевый соус"
    ),
    FoodItem(
        name="Грибной жюльен",
        calories=260,
        protein=10.0,
        carbs=12.0,
        fats=18.0,
        category="вегетарианский",
        description="Нежная закуска",
        recipe="Шампиньоны, лук, сметана, сыр, запекать в кокотницах"
    ),
    FoodItem(
        name="Спагетти с песто",
        calories=380,
        protein=12.0,
        carbs=50.0,
        fats=15.0,
        category="вегетарианский",
        description="Итальянская паста",
        recipe="Спагетти, соус песто, помидоры черри, пармезан, кедровые орехи"
    )
]
# Ключевые слова для категорий
CATEGORY_KEYWORDS = {
    "завтрак": ["завтрак", "утро", "кофе", "каша", "омлет"],
    "обед": ["обед", "день", "суп", "горячее", "первое"],
    "ужин": ["ужин", "вечер", "ночь", "легкий", "салат"],
    "перекус": ["перекус", "снек", "фрукт", "йогурт", "творог"]
}

@app.get("/")
def read_root():
    return {"message": "Food AI Assistant API работает!"}

@app.get("/test")
def test():
    return {"status": "ok", "food": "пицца", "calories": 300}

# ВАЖНО: Этот endpoint должен быть!
@app.post("/api/recommend")
def recommend_food(request: FoodRequest):
    """Основная функция рекомендаций"""
    query = request.query.lower()
    
    # 1. Определяем категорию по запросу
    category = "обед"  # по умолчанию
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in query for keyword in keywords):
            category = cat
            break
    
    # 2. Фильтруем по категории
    filtered_foods = [f for f in FOOD_DATABASE if f.category == category]
    
    # 3. Простая логика: подбираем блюда по калориям
    target_calories = request.user_calories / 3
    suitable_foods = [
        f for f in filtered_foods 
        if abs(f.calories - target_calories) < 150
    ]
    
    if not suitable_foods:
        suitable_foods = filtered_foods
    
    # 4. Выбираем случайное блюдо
    recommendation = random.choice(suitable_foods)
    
    return {
        "recommendation": recommendation,
        "query_analysis": {
            "original_query": request.query,
            "detected_category": category,
            "target_calories": target_calories
        },
        "alternatives": suitable_foods[:3]
    }

@app.get("/api/foods/all")
def get_all_foods(category: str = None):
    """Получить все блюда (можно фильтровать по категории)"""
    if category:
        filtered = [f for f in FOOD_DATABASE if f.category == category]
        return {"count": len(filtered), "foods": filtered}
    return {"count": len(FOOD_DATABASE), "foods": FOOD_DATABASE}

@app.get("/api/foods/categories")
def get_categories():
    """Получить все доступные категории"""
    categories = list(set(food.category for food in FOOD_DATABASE))
    return {"categories": categories}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
