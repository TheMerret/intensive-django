from datetime import datetime


def server_datetime(request):
    return {"server_datetime": datetime.now()}
