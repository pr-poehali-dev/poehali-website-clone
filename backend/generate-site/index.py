import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any
import random

ENERGY_COST = 20

def generate_site_html(prompt: str) -> str:
    '''Generate beautiful HTML site using smart templates'''
    
    prompt_lower = prompt.lower()
    colors = [
        ('blue', 'indigo', '🌊'),
        ('purple', 'pink', '💜'),
        ('green', 'teal', '🌿'),
        ('orange', 'red', '🔥'),
        ('cyan', 'blue', '⚡')
    ]
    color1, color2, emoji = random.choice(colors)
    
    sections_html = ''
    
    if any(w in prompt_lower for w in ['магазин', 'товар', 'продукт', 'купить']):
        sections_html += f'''
    <section class="py-20 bg-gray-50">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-12">Наши товары</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all">
                    <div class="text-6xl mb-4 text-center">📦</div>
                    <h3 class="text-2xl font-bold mb-2">Товар 1</h3>
                    <p class="text-gray-600 mb-4">Описание товара</p>
                    <div class="text-3xl font-bold text-{color1}-600 mb-4">1990₽</div>
                    <button class="w-full bg-{color1}-600 text-white py-3 rounded-lg hover:bg-{color1}-700">Купить</button>
                </div>
                <div class="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all">
                    <div class="text-6xl mb-4 text-center">🎁</div>
                    <h3 class="text-2xl font-bold mb-2">Товар 2</h3>
                    <p class="text-gray-600 mb-4">Описание товара</p>
                    <div class="text-3xl font-bold text-{color1}-600 mb-4">2990₽</div>
                    <button class="w-full bg-{color1}-600 text-white py-3 rounded-lg hover:bg-{color1}-700">Купить</button>
                </div>
                <div class="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all">
                    <div class="text-6xl mb-4 text-center">⭐</div>
                    <h3 class="text-2xl font-bold mb-2">Товар 3</h3>
                    <p class="text-gray-600 mb-4">Описание товара</p>
                    <div class="text-3xl font-bold text-{color1}-600 mb-4">3990₽</div>
                    <button class="w-full bg-{color1}-600 text-white py-3 rounded-lg hover:bg-{color1}-700">Купить</button>
                </div>
            </div>
        </div>
    </section>'''
    
    if any(w in prompt_lower for w in ['услуг', 'сервис', 'цен', 'тариф']):
        sections_html += f'''
    <section class="py-20 bg-white">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-12">Наши услуги</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="border-2 border-gray-200 rounded-2xl p-8 hover:border-{color1}-600 transition-all">
                    <h3 class="text-2xl font-bold mb-4">Базовый</h3>
                    <div class="text-4xl font-bold text-{color1}-600 mb-6">5000₽<span class="text-lg text-gray-500">/мес</span></div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center"><span class="mr-2">✓</span> Функция 1</li>
                        <li class="flex items-center"><span class="mr-2">✓</span> Функция 2</li>
                        <li class="flex items-center"><span class="mr-2">✓</span> Функция 3</li>
                    </ul>
                    <button class="w-full bg-{color1}-600 text-white py-3 rounded-lg hover:bg-{color1}-700">Выбрать</button>
                </div>
                <div class="border-2 border-{color1}-600 rounded-2xl p-8 transform scale-105 shadow-xl">
                    <div class="bg-{color1}-600 text-white text-sm font-bold px-3 py-1 rounded-full inline-block mb-4">Популярный</div>
                    <h3 class="text-2xl font-bold mb-4">Про</h3>
                    <div class="text-4xl font-bold text-{color1}-600 mb-6">9000₽<span class="text-lg text-gray-500">/мес</span></div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center"><span class="mr-2">✓</span> Всё из Базового</li>
                        <li class="flex items-center"><span class="mr-2">✓</span> Функция 4</li>
                        <li class="flex items-center"><span class="mr-2">✓</span> Функция 5</li>
                    </ul>
                    <button class="w-full bg-{color1}-600 text-white py-3 rounded-lg hover:bg-{color1}-700">Выбрать</button>
                </div>
                <div class="border-2 border-gray-200 rounded-2xl p-8 hover:border-{color1}-600 transition-all">
                    <h3 class="text-2xl font-bold mb-4">Премиум</h3>
                    <div class="text-4xl font-bold text-{color1}-600 mb-6">15000₽<span class="text-lg text-gray-500">/мес</span></div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center"><span class="mr-2">✓</span> Всё из Про</li>
                        <li class="flex items-center"><span class="mr-2">✓</span> Функция 6</li>
                        <li class="flex items-center"><span class="mr-2">✓</span> Приоритет поддержки</li>
                    </ul>
                    <button class="w-full bg-{color1}-600 text-white py-3 rounded-lg hover:bg-{color1}-700">Выбрать</button>
                </div>
            </div>
        </div>
    </section>'''
    
    if not sections_html:
        sections_html = f'''
    <section class="py-20 bg-white">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-12">Преимущества</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="text-center p-8">
                    <div class="text-6xl mb-4">{emoji}</div>
                    <h3 class="text-2xl font-bold mb-4">Быстро</h3>
                    <p class="text-gray-600">Мгновенное решение ваших задач</p>
                </div>
                <div class="text-center p-8">
                    <div class="text-6xl mb-4">✨</div>
                    <h3 class="text-2xl font-bold mb-4">Качественно</h3>
                    <p class="text-gray-600">Профессиональный подход к делу</p>
                </div>
                <div class="text-center p-8">
                    <div class="text-6xl mb-4">🎯</div>
                    <h3 class="text-2xl font-bold mb-4">Надёжно</h3>
                    <p class="text-gray-600">Гарантия результата</p>
                </div>
            </div>
        </div>
    </section>'''
    
    title = ' '.join(prompt.split()[:3]) if len(prompt.split()) > 3 else prompt
    
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="antialiased">
    <header class="bg-gradient-to-r from-{color1}-600 to-{color2}-600 text-white py-24">
        <div class="container mx-auto px-4 text-center">
            <div class="text-7xl mb-6">{emoji}</div>
            <h1 class="text-5xl md:text-6xl font-bold mb-6">{prompt}</h1>
            <p class="text-xl md:text-2xl mb-8 opacity-90">Воплощаем идеи в реальность</p>
            <button class="bg-white text-{color1}-600 font-bold py-4 px-10 rounded-full hover:shadow-2xl transition-all text-lg">
                Начать сейчас
            </button>
        </div>
    </header>

{sections_html}

    <section class="bg-gradient-to-r from-{color1}-600 to-{color2}-600 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-4xl font-bold mb-6">Готовы начать?</h2>
            <p class="text-xl mb-8 opacity-90">Присоединяйтесь к нам прямо сейчас</p>
            <button class="bg-white text-{color1}-600 font-bold py-4 px-10 rounded-full hover:shadow-2xl transition-all text-lg">
                Связаться с нами
            </button>
        </div>
    </section>

    <footer class="bg-gray-900 text-white py-12">
        <div class="container mx-auto px-4 text-center">
            <p class="text-lg mb-2">© 2024 {title}</p>
            <p class="text-gray-400">Создано на POEHALI.DEV</p>
        </div>
    </footer>
</body>
</html>'''
    
    return html


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Generate beautiful website using smart templates
    Args: event - dict with httpMethod, body (user_id, prompt)
    Returns: HTTP response with generated HTML code
    '''
    method: str = event.get('httpMethod', 'POST')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-User-Id',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    if method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    body_data = json.loads(event.get('body', '{}'))
    user_id = body_data.get('user_id')
    prompt = body_data.get('prompt', '').strip()
    
    if not user_id or not prompt:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'user_id and prompt required'})
        }
    
    dsn = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(dsn)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT energy_balance FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        
        if not user:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'User not found'})
            }
        
        if user['energy_balance'] < ENERGY_COST:
            return {
                'statusCode': 403,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({
                    'error': 'Not enough energy',
                    'required': ENERGY_COST,
                    'current': user['energy_balance']
                })
            }
        
        generated_html = generate_site_html(prompt)
        
        new_balance = user['energy_balance'] - ENERGY_COST
        cur.execute(
            "UPDATE users SET energy_balance = %s WHERE id = %s",
            (new_balance, user_id)
        )
        conn.commit()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'success': True,
                'html': generated_html,
                'energy_used': ENERGY_COST,
                'energy_remaining': new_balance
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'error': 'Generation failed',
                'details': str(e)
            })
        }
    
    finally:
        cur.close()
        conn.close()