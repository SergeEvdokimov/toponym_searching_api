import os
import sys
import pygame
import requests
from adjust_ll_span import adjust_ll_span


def show_map(ll_spn, map_type="map", add_params=None):
    map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        continue

    pygame.quit()
    os.remove(map_file)


place = " ".join(sys.argv[1:])

if not place:
    print('Введите данные')
    sys.exit(0)

ll, spn = adjust_ll_span(place)
ll_spn = f"ll={ll}&spn={spn}"
show_map(ll_spn, "map", add_params=f"pt={ll}")
