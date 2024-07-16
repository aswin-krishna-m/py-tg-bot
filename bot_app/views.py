from django.http import HttpResponse
from django.shortcuts import render,redirect
from .bot import bot_tele,API_KEY,WEBHOOK_HOST
from .modules.my_constants import db_connection,shows
import json,asyncio,requests
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):
    db, conn = db_connection()
    conn.execute(f"SELECT show_id, series, title FROM {shows}")
    s_list = conn.fetchall()
    db.close()

    paginator = Paginator(s_list, 50)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'shows_list': page_obj})

def setwebhook(request):
    webhook_url = f'https://{WEBHOOK_HOST}/webhook'
    set_webhook_url = f'https://api.telegram.org/bot{API_KEY}/setWebhook'
    
    response = requests.post(set_webhook_url, data={'url': webhook_url})
    
    if response.status_code == 200:
        print('Webhook set successfully')
    else:
        print('Failed to set webhook:', response.content)
    return redirect(index)


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = request.body
        res = json.loads(data.decode('utf-8'))
        asyncio.run(bot_tele(res))
        return HttpResponse("OK")
    else:
        return HttpResponse("invalid response!!!")