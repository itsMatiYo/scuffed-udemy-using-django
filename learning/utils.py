import requests
from decouple import config

BASE_AUTH = config('BASE_AUTH')
HOST = config('HOST')
TOKEN = config('TOKEN')


def update_roles():
    with open("settings.ini", 'r') as reader:
        get_all = reader.readlines()
    response = requests.post(
        url=HOST + "/admin/role", headers={'auth_basic': BASE_AUTH, 'Authorization': TOKEN, }
    )
    if response.json()['status'] == True:
        roles = response.json()['data']
        for role in roles:
            if role['name'] == "teacher":
                ROLE_ID_TEACHER = role['id']
            if role['name'] == "student":
                ROLE_ID_STUDENT = role['id']
            if role['name'] == "adviser":
                ROLE_ID_ADVISER = role['id']
        with open('settings.ini', 'w') as reader:
            for i, line in enumerate(get_all, 1):
                if i == 8:
                    reader.writelines("ROLE_ID_TEACHER = " +
                                      ROLE_ID_TEACHER+"\n")
                elif i == 9:
                    reader.writelines("ROLE_ID_STUDENT = " +
                                      ROLE_ID_STUDENT+"\n")
                elif i == 10:
                    reader.writelines("ROLE_ID_ADVISER = " +
                                      ROLE_ID_ADVISER+"\n")
                else:
                    reader.writelines(line)
        print("************Roles Update************")
    else:
        print(response.json())
        print("************Roles not Update************")
