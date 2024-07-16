from django.http import HttpResponse
from django.shortcuts import render
from .bot import bot_tele
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

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = request.body
        res = json.loads(data.decode('utf-8'))
        asyncio.run(bot_tele(res))
        return HttpResponse("OK")
    else:
        return HttpResponse("invalid response!!!")