import datetime
import requests
import time
from math import radians, cos, sin, asin, sqrt
import time
import String
from message import Message
import _
import openpyxl
import json
import schedule
from admin import *
from params import Params
from String import *
# choose suranme путается метод и переменная

"""При перезвпуске сервера всегда будет лист 2022-2023, надо менять лист при перезапуске"""
"""Правила в присылаемом файле без формул и переносов, при перезапуске сервера не забыть лист на дейтсвущий,  фамилии бех проблеоов справа слева"""
TOKEN = _.token
sheetname = "2022-2023"
chat_id_column = "A"
course_column = "B"
surname_column = "C"
advantage_column = "D"
URL = 'https://api.telegram.org/bot'
radius = 0.3

process = {}


def get_updates(offset=0):
    result = requests.get(f'{URL + TOKEN}/getUpdates?offset={offset}').json()
    return result['result']


def send_message(chat_id, params):
    requests.get(f'{URL + TOKEN}/sendMessage?chat_id={chat_id}', params=params.get_params())


def is_person_near(location):
    center = 60.005143, 30.372276
    center_point = [{latitude: center[0], longitude: center[1]}]
    test_point = [location]
    lat1 = center_point[0][latitude]
    lon1 = center_point[0][longitude]
    lat2 = test_point[0][latitude]
    lon2 = test_point[0][longitude]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r <= radius


def lesson_started():
    book = openpyxl.load_workbook(filename)
    chat_ids = [i.value for i in book[sheetname][chat_id_column][1:]]
    count = 1
    for i in chat_ids:
        if i != "" and i is not None:
            if count % 15 == 0:
                time.sleep(2)
            send_message(i, Params(text=lesson_started_command))
            count += 1


def mark_user(chat_id, surname=None, current_data=None):
    today_data = datetime.date.today()
    book = openpyxl.load_workbook(filename)
    sheet = book[sheetname]
    res_row = 0
    for row in sheet.iter_rows():
        if row[0].value == chat_id or row[2].value == surname:
            res_row = str(row[0].row)
            break
    for row in sheet.iter_rows():
        for title in row:
            if isinstance(title.value, datetime.datetime):
                data = datetime.date(title.value.year, title.value.month, title.value.day)
                if (data == today_data and current_data is None) or data == current_data and res_row != "0":
                    sheet[title.column_letter + res_row].value = "+"
                    book.save(filename)
                    return True
        return False


def choose_surname(chat_id, text):
    book = openpyxl.load_workbook(filename)
    sheet = book[sheetname]
    selected_course = text.split()[0]
    persons = []
    for i in sheet[course_column][1:]:
        if str(i.value) == selected_course:
            persons.append(sheet[surname_column + str(i.row)].value)
    send_message(chat_id, Params(text=choose_surname_command,
                                 reply_markup=create_reply_markup(chunked_list(sorted(persons)))))


def chunked_list(list):
    result = []
    for i in range(0, len(list), 3):
        if i + 2 < len(list):
            result.append([list[i], list[i + 1], list[i + 2]])
    if len(list) % 3 == 1:
        result.append([list[-1]])
    if len(list) % 3 == 2:
        result.append([list[-2], list[-1]])
    return result


def find_next_column(n):
    if isinstance(n, str):
        if n >= "Z":
            return "A" + chr(ord(n) - 25)
        else:
            return chr(ord(n) + 1)
    elif isinstance(n, int):
        if n >= 26:
            return "A" + chr(ord("A") + n % 26)
        else:
            return chr(ord("A") + n)


def create_reply_markup(list):
    return json.dumps({'keyboard': list,
                       'resize_keyboard': True,
                       'one_time_keyboard': True,
                       'selective': True})


def is_user_authorization(chat_id):
    book = openpyxl.load_workbook(filename)
    return chat_id in [i.value for i in book[sheetname][chat_id_column]][1:]


def get_surname_by_chat_id(chat_id):
    book = openpyxl.load_workbook(filename)
    sheet = book[sheetname]
    chat_ids = [i.value for i in book[sheetname][chat_id_column]][1:]
    return sheet[surname_column + str(2 + chat_ids.index(chat_id))].value


def get_chat_id_field_by_surname(surname):
    book = openpyxl.load_workbook(filename)
    sheet = book[sheetname]
    all_surname = [i.value.capitalize().strip() for i in sheet[surname_column][1:]]
    surname_index = all_surname.index(surname.capitalize().strip())
    return sheet[chat_id_column + str(2 + surname_index)]


def is_surname_exist(surname):
    book = openpyxl.load_workbook(filename)
    sheet = book[sheetname]
    return surname.capitalize().strip() in [i.value.capitalize().strip() for i in sheet[surname_column][1:]]


def start(message):
    chat_id = message.get_chat_id()
    if message.is_text_message():
        if start_command == message.get_text():
            send_message(chat_id,  Params(text=choose_course,
                                          reply_markup=create_reply_markup([[first_course, second_course]])))
        elif course in message.get_text():
            choose_surname(chat_id, message.get_text())
        else:
            book = openpyxl.load_workbook(filename)
            sheet = book[sheetname]
            if is_surname_exist(message.get_text()):
                chat_id_field = get_chat_id_field_by_surname(message.get_text())
                if chat_id_field.value is None:
                    sheet[chat_id_field.coordinate].value = chat_id
                    book.save(filename)
                    reply_markup = json.dumps({remove_keyboard: True})
                    send_message(chat_id, Params(text=authorization_success, reply_markup=reply_markup))
                else:
                    send_message(chat_id, Params(text=surname_used_by_other))
            else:
                send_message(chat_id, Params(text=surname_enter_incorrect))


def run():
    # schedule.every().saturday.at("18:00").do(lesson_started())
    while True:
        schedule.run_pending()
        try:
            update_id = get_updates()[-1]["update_id"]
            while True:
                messages = get_updates(update_id)
                for message_js in messages:
                    if update_id < message_js["update_id"]:
                        update_id = message_js["update_id"]
                        message = Message(message_js)
                        if message.get_message_type() == "message":
                            chat_id = message.get_chat_id()
                            if message.get_username() in admins:
                                admin_method(message)
                            elif not is_user_authorization(chat_id):
                                start(message)
                            elif message.is_location_message():
                                if 18 <= time.localtime().tm_hour <= 23:
                                    if message.is_live_location():
                                        if is_person_near(message.get_location()):
                                            if mark_user(chat_id):
                                                send_message(chat_id, Params(text=correct_input))
                                            else:
                                                reply_markup = json.dumps({remove_keyboard: True})
                                                send_message(chat_id, Params(text=no_lesson_today,
                                                                             reply_markup=reply_markup))
                                        else:
                                            send_message(chat_id, Params(
                                                text=f"Для отметки о посещении необходимо быть в радиусе "
                                                     f"{int(radius * 1000)} метров"))
                                    else:
                                        send_message(chat_id, Params(text=notification_of_location))
                                        send_media(chat_id, requirements_of_location_message, "photo")
                                else:
                                    send_message(chat_id, Params(text=notification_of_time))
                            else:
                                send_message(chat_id, Params(text="Вы вошли под фамилией " +
                                                                      get_surname_by_chat_id(chat_id)))
        except Exception as e:
            time.sleep(1)
            print(e)


if __name__ == '__main__':
    run()
