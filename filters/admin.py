from config import ADMINS

#ID_TG Админа
ADMIN = ADMINS

#Проверка, является ли пользователь админом
def check_admin(user_id):
    for i in ADMIN:
        if str(user_id) == str(i): return True

    return False
