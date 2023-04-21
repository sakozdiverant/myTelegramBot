
def config_read(seach):
    spisok = open(".//config.txt", 'r', encoding="utf-8")
    spisok_config = ['host', 'TOKEN', 'to_emails', 'Button_name_1', 'Button_name_2', 'Button_name_3', 'Button_name_4',
            'Button_send_1', 'Button_send_2', 'Button_send_3', 'Button_send_4', 'Button_down_1', 'Button_down_2',
            'Re_registration', 'Registration', 'Incorrect_address', 'Hello']
    spisok = spisok.read()

    if seach in spisok_config:
        num = spisok.find(seach)
        num_end = spisok.find('\n', num)
        if num_end == -1:
            return spisok[num + len(seach) + 3:len(spisok)]
        else:
            return spisok[num + len(seach) + 3:num_end]
    else:
        return "Неизвестный конфиг!!!"

def admin():
    spisok = open(".//admin.cfg", 'r', encoding="utf-8")
    spisok = spisok.readlines()
    list = []
    for i in spisok:
        list.append(int(i.replace('\n', '')))
    return list

def to_slovar():
    slovar = {}
    spisok = open(".//to.csv", 'r')
    spisok = spisok.readlines()
    list = []
    for i in spisok:
        add = (i.replace('\n', '')).split(';')
        slov = {int(add[1]): [add[0], add[2], add[3]]}
        slovar.update(slov)
    return slovar

