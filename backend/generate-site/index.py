import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any
from groq import Groq

ENERGY_COST = 20
# Force redeploy to pick up new GROQ_API_KEY secret

def generate_site_with_ai(prompt: str) -> str:
    '''Generate HTML site using Groq AI'''
    
    groq_api_key = os.environ.get('GROQ_API_KEY')
    if not groq_api_key:
        raise ValueError('GROQ_API_KEY not configured')
    
    client = Groq(api_key=groq_api_key)
    
    system_prompt = '''Ты — эксперт по созданию красивых современных landing page сайтов.
Создай ПОЛНЫЙ HTML код сайта на основе запроса пользователя.

ТРЕБОВАНИЯ:
1. Используй Tailwind CSS через CDN: <script src="https://cdn.tailwindcss.com"></script>
2. Используй современный дизайн с градиентами, тенями, анимациями
3. Шрифт Google Fonts (Inter или Poppins)
4. Адаптивный дизайн (mobile-first)
5. Минимум 3-4 секции (hero, features, cta, footer)
6. Используй красивые emoji вместо иконок
7. Яркие цвета и современная типографика
8. Обязательно добавь meta теги, title, viewport

ВЕРНИ ТОЛЬКО КОД HTML, без объяснений, markdown или других текстов.
Начни с <!DOCTYPE html> и закончи </html>'''
    
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Создай сайт: {prompt}"}
        ],
        temperature=0.8,
        max_tokens=8000
    )
    
    html = response.choices[0].message.content.strip()
    
    if html.startswith('```html'):
        html = html[7:]
    if html.startswith('```'):
        html = html[3:]
    if html.endswith('```'):
        html = html[:-3]
    
    return html.strip()


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Generate website using Groq AI based on user prompt
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
        
        generated_html = generate_site_with_ai(prompt)
        
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