import requests
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def adjust_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    envelope = toponym["boundedBy"]["Envelope"]

    left, bottom = envelope["lowerCorner"].split()
    right, top = envelope["upperCorner"].split()

    width = abs(float(left) - float(right))
    height = abs(float(top) - float(bottom))

    return ",".join(toponym["Point"]["pos"].split()), f"{width/2},{height/2}"  # ll, span


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_request, params=params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request} \nHttp статус: {response.status_code} ({response.reason})""")

    features = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return features if features else None
