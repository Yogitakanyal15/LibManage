from main import getconnection
from colorama import Fore, Style, init
init(autoreset=True)
def admin_login():
    count = 0
    while count < 3:
        name = input(Fore.blue+"Enter your name: ")
        password = input(Fore.blue+"Enter your password: ")
        
        db = getconnection()
        cursor = db.cursor()
        sql = "SELECT password FROM admin WHERE username = %s"
        cursor.execute(sql, (name,))
        lst = cursor.fetchall()

        if len(lst) == 0:
            print("No such admin exists!")
        else:
            passw = lst[0][0]
            if passw == password:
                print(Fore.green+"WELCOME!")
                return True
            else:
                print(Fore.red+"Wrong password!")
        
        count += 1
        #print(f"Attempt {count}/3\n")

    print(Fore.yellow+"You have reached the maximum login attempts!")
    return False
