import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any
import random

ENERGY_COST = 20

def generate_site_html(prompt: str) -> str:
    '''Generate HTML site based on prompt using templates'''
    
    prompt_lower = prompt.lower()
    
    colors = [
        ('blue', 'purple', '#3B82F6', '#9333EA'),
        ('green', 'teal', '#10B981', '#14B8A6'),
        ('pink', 'rose', '#EC4899', '#F43F5E'),
        ('orange', 'amber', '#F97316', '#F59E0B'),
        ('indigo', 'violet', '#6366F1', '#8B5CF6')
    ]
    
    color1, color2, hex1, hex2 = random.choice(colors)
    
    sections = []
    
    if any(word in prompt_lower for word in ['кофе', 'кафе', 'ресторан', 'кофейня', 'еда']):
        sections.append(f'''
        <section class="py-20 bg-gradient-to-r from-{color1}-50 to-{color2}-50">
            <div class="container mx-auto px-4">
                <h2 class="text-4xl font-bold text-center mb-12">Наше меню</h2>
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-shadow">
                        <h3 class="text-2xl font-bold mb-4">Эспрессо</h3>
                        <p class="text-gray-600 mb-4">Классический крепкий кофе</p>
                        <p class="text-3xl font-bold text-{color1}-600">150₽</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-shadow">
                        <h3 class="text-2xl font-bold mb-4">Капучино</h3>
                        <p class="text-gray-600 mb-4">С нежной молочной пенкой</p>
                        <p class="text-3xl font-bold text-{color1}-600">200₽</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-shadow">
                        <h3 class="text-2xl font-bold mb-4">Латте</h3>
                        <p class="text-gray-600 mb-4">Мягкий кофе с молоком</p>
                        <p class="text-3xl font-bold text-{color1}-600">220₽</p>
                    </div>
                </div>
            </div>
        </section>
        ''')
    
    if any(word in prompt_lower for word in ['форма', 'заказ', 'контакт', 'связ']):
        sections.append(f'''
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4 max-w-2xl">
                <h2 class="text-4xl font-bold text-center mb-12">Оставьте заявку</h2>
                <form class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium mb-2">Имя</label>
                        <input type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-{color1}-500 focus:border-transparent" placeholder="Ваше имя">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Email</label>
                        <input type="email" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-{color1}-500 focus:border-transparent" placeholder="your@email.com">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Сообщение</label>
                        <textarea class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-{color1}-500 focus:border-transparent" rows="4" placeholder="Ваше сообщение"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-gradient-to-r from-{color1}-600 to-{color2}-600 text-white font-bold py-3 px-6 rounded-lg hover:shadow-xl transition-shadow">
                        Отправить
                    </button>
                </form>
            </div>
        </section>
        ''')
    
    if any(word in prompt_lower for word in ['портфолио', 'работ', 'проект', 'галерея']):
        sections.append(f'''
        <section class="py-20 bg-gray-50">
            <div class="container mx-auto px-4">
                <h2 class="text-4xl font-bold text-center mb-12">Наши работы</h2>
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-shadow">
                        <div class="h-48 bg-gradient-to-br from-{color1}-400 to-{color2}-400"></div>
                        <div class="p-6">
                            <h3 class="text-xl font-bold mb-2">Проект 1</h3>
                            <p class="text-gray-600">Описание проекта</p>
                        </div>
                    </div>
                    <div class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-shadow">
                        <div class="h-48 bg-gradient-to-br from-{color2}-400 to-{color1}-400"></div>
                        <div class="p-6">
                            <h3 class="text-xl font-bold mb-2">Проект 2</h3>
                            <p class="text-gray-600">Описание проекта</p>
                        </div>
                    </div>
                    <div class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-shadow">
                        <div class="h-48 bg-gradient-to-br from-{color1}-400 to-{color2}-400"></div>
                        <div class="p-6">
                            <h3 class="text-xl font-bold mb-2">Проект 3</h3>
                            <p class="text-gray-600">Описание проекта</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        ''')
    
    if not sections:
        sections.append(f'''
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4 text-center">
                <h2 class="text-4xl font-bold mb-6">О нас</h2>
                <p class="text-xl text-gray-600 max-w-3xl mx-auto mb-12">
                    {prompt}
                </p>
                <div class="grid md:grid-cols-3 gap-8 mt-12">
                    <div class="p-6">
                        <div class="text-5xl mb-4">⚡</div>
                        <h3 class="text-xl font-bold mb-2">Быстро</h3>
                        <p class="text-gray-600">Мгновенная обработка</p>
                    </div>
                    <div class="p-6">
                        <div class="text-5xl mb-4">🎨</div>
                        <h3 class="text-xl font-bold mb-2">Красиво</h3>
                        <p class="text-gray-600">Современный дизайн</p>
                    </div>
                    <div class="p-6">
                        <div class="text-5xl mb-4">🚀</div>
                        <h3 class="text-xl font-bold mb-2">Надёжно</h3>
                        <p class="text-gray-600">Проверенные решения</p>
                    </div>
                </div>
            </div>
        </section>
        ''')
    
    title = prompt.split()[0].capitalize() if prompt else "Мой сайт"
    
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="antialiased">
    <header class="bg-gradient-to-r from-{color1}-600 to-{color2}-600 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-5xl md:text-6xl font-bold mb-6">{prompt}</h1>
            <p class="text-xl md:text-2xl opacity-90 mb-8">Создано на POEHALI.DEV</p>
            <button class="bg-white text-{color1}-600 font-bold py-3 px-8 rounded-lg hover:shadow-2xl transition-shadow text-lg">
                Начать работу
            </button>
        </div>
    </header>

    {''.join(sections)}

    <footer class="bg-gray-900 text-white py-12">
        <div class="container mx-auto px-4 text-center">
            <p class="text-lg">&copy; 2024 {title}. Все права защищены.</p>
            <p class="text-gray-400 mt-2">Сделано с ❤️ на POEHALI.DEV</p>
        </div>
    </footer>
</body>
</html>'''
    
    return html


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Generate website using templates based on user prompt
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
    
    finally:
        cur.close()
        conn.close()
