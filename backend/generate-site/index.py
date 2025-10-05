import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any
import urllib.request
import urllib.error

ENERGY_COST = 20

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Generate website using AI based on user prompt
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
        
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'OpenAI API key not configured'})
            }
        
        system_prompt = """Ты - эксперт по созданию современных веб-сайтов. 
Создавай красивый, адаптивный HTML код с встроенными CSS стилями.
Используй современный дизайн с градиентами, анимациями и яркими цветами.
Код должен быть полностью готов к использованию - один HTML файл со всем необходимым.
Используй Tailwind CSS CDN для стилизации.
Ответ должен содержать ТОЛЬКО HTML код без дополнительных объяснений."""

        request_body = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Создай сайт: {prompt}"}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        req = urllib.request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=json.dumps(request_body).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                generated_html = response_data['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': f'OpenAI API error: {error_body}'})
            }
        
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
