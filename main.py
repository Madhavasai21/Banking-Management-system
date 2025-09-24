import mysql.connector as db # Mysql connector
from tabulate import tabulate as tb # Tabulate for show data in table formates
from datetime import datetime as dt # To generate transaction id's 
import random 
import time
from colorama import Fore, Back, Style, init #To print Colored outputs
init(autoreset=True)
con=db.connect(user='root',#user_name
           password='Your_password',#password
           host='localhost',#host
           database='Bank')#database
cur=con.cursor()
def user_registration(): #new_user_registration
        lis=['savings','current','salary','fixed deposit']
        while True:
            user_name=input("\nEnter user_name:")
            if not user_name.isalpha():
                print(Fore.RED + "Name should contains only Alphabets")
            else:
                break
        while True:
            account_type=input("\nChoose Account_type--Savings/Current/Salary/Fixed Deposit--: ").lower()
            if account_type in lis:
                while True:
                    phone_no=input("\nEnter phone number: ")
                    if  (not phone_no.isdigit()) or (not phone_no.startswith(('6','7','8','9'))) or (len(phone_no)!=10):
                        print(Fore.RED + "\nInvalid phone number must be 10 digits and starts with[6,7,8,9] only")
                    else:
                        break
                while True:#pin validation
                    pin=input("\nPlease Create pin: ")
                    if len(pin)!=4 or not pin.isdigit():
                        print(Fore.RED + "\npin muust be 4 digits and digits only")
                    else:
                        break
                while True:#intial deposit
                    intial_amount=input("\nplease deposit minimum amount of 500 to open_Account: ")
                    if not intial_amount.isdigit():
                        print(Fore.RED + "\nplease select amount in correct type")
                    else:
                        intial_amount=int(intial_amount)
                        if intial_amount>=500:#insert details into db
                            cur.execute('INSERT INTO users(User_name,Account_Type,Phone_no,Pin,Amount) values(%s,%s,%s,%s,%s)'\
                                        ,(user_name,account_type,phone_no,pin,intial_amount))
                            con.commit()
                            cur.execute('select account_number from users order by account_number desc limit 1;')
                            data=cur.fetchone()
                            now=dt.now()
                            tx_id='TXN'+now.strftime('%Y%m%d%H%M%S')
                            for ac_no in data:
                                print(Fore.GREEN + "\nUser account created successfuly")
                                print(Fore.LIGHTYELLOW_EX + "\nYour account_number is:",ac_no)
                                print("\n*********Welcome to our Bank**********")
                                res=amount(ac_no)
                                cur.execute('insert into Transactions (transaction_id,Account_number,Transaction_type,Transaction_amount,Available_amount)values(%s,%s,%s,%s,%s)',\
                                            (tx_id,ac_no,'CREDIT',intial_amount,(res)))
                                con.commit()
                                return
                        else:
                            print(Fore.RED + "\nThe minimum amount to open account is 500")
            else:
                print(Fore.RED + "\nplease select valid account_type")
def amount(account_number):#Current Balance in user Bank_account
    cur.execute('select amount from users where account_number=%s',(account_number,))
    data=cur.fetchone()
    for d in data:
        return d
def user_login():#user login
    global account_number
    while True:
        account_number=input("\nEnter account_number:")
        if not account_number.isdigit():
            print(Fore.RED + "Please check account_number once (only digits allowed)")
        elif len(account_number)!=14:
            print(Fore.RED + "Check account_number must be 14 digits only")
        else:
            account_number=int(account_number)
            cur.execute('select * from users where account_number=%s',(account_number,))
            data=cur.fetchone()
            if data:
                print(Fore.GREEN + "Account_found:",data[0])
            else:
                print(Fore.GREEN + "Account Not found Please check")
                continue
            while True:
                c=3
                while c>0:
                        pin=input("\nEnter pin number:")
                        if len(pin)!=4 or not pin.isdigit():
                            print(Fore.RED + "\nplease check pin and enter pin(pin must be 4 digits)")
                            c-=1
                            print(f"Attempts left {c}")
                            continue
                        cur.execute('select * from users where Account_number=%s and pin=%s',(account_number,pin))
                        d=cur.fetchone()
                        if d:
                            print(Fore.GREEN + f"\nWelcome {d[0]}")
                            user_operations()
                            return
                        else:
                            print(Fore.RED + "Invalid credentials Check details again\n")
                            c-=1
                            print(Fore.RED + f"\n Attempts left {c}\n")
                else:
                        print(Fore.RED + "To many Attempts")
                        return
def statement(ac_no): #statement
    while True:
        try:
            from_date=input("Enter From date of transactions (YYYY-MM-DD): ")
            to_date=input("Enter  To date of transactions (YYYY-MM-DD): ")
            try:
                dt.strptime(from_date, "%Y-%m-%d")
                dt.strptime(to_date, "%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "\nInvalid date format! Please enter in YYYY-MM-DD format.")
                continue
            cur.execute('select * from transactions Where account_number=%s and date(Transaction_time)>=%s and date(transaction_time)<=%s',\
                    (ac_no,from_date,to_date))
            data=cur.fetchall()
            headers=[desc[0] for desc in cur.description]
            if data:
                print(tb(data,headers=headers,tablefmt='fancy_grid'))
                break
            else:
                print(Fore.BLUE + "\nNo transactions Happend on that date")
                break
        except:
            print("Db Error")
def user_operations():#user operations
    while True:
        print(Fore.GREEN + """
======User Actions=======
        1:view_details
        2:Check Balance
        3:Pinchage
        4:Credit
        5:Debit
        6:Statement
        7:Transfer
        8:Logout
=========================
                 """)
        ch=input("\nEnter choice:")
        if ch.isalpha():
            print(Fore.RED + "Please choose the correct  one option(1-8).")
        elif ch=='1':#view_details
              cur.execute('select * from users where account_number=%s',(account_number,))
              row=cur.fetchone()
              headers=[desc[0] for desc in cur.description]
              if row:
                  print(tb([row],headers=headers,tablefmt='fancy_grid'))
        elif ch=='2':#check balance
            res=amount(account_number)#assing variable to store return value current_Amount
            headers=['Current_Amount']
            if res:
                print(tb([[res]],headers=headers,tablefmt='fancy_grid'))
        elif ch=='3':#Pin change
            while True:
                pin=input("\nEnter current pin: ")
                if (not pin.isdigit()) or (len(pin)!=4):
                    print(Fore.RED + "Invalid Pin must be digits and 4 digits only")
                else:
                    cur.execute('select pin from users where account_number=%s and pin=%s',(account_number,pin))
                    data=cur.fetchone()
                    if data:
                        otp=str(random.randint(1000,9999))
                        print("Sending otp...")
                        time.sleep(3)
                        print(Fore.BLUE + f"\nYour OTP is: {otp}")
                        user_otp=input("\nEnter otp:")
                        if user_otp!=otp:
                            print(Fore.RED + "\nInvalid OTP try again")
                            break
                        while True:
                            new_pin=input('\nEnter new pin_number:')
                            if (not new_pin.isdigit()) or len(new_pin)!=4:
                                print(Fore.RED + "Invalid Pin must be digits and 4 digits only")
                            else:
                                cur.execute('update users set pin=%s where account_number=%s',(new_pin,account_number))
                                con.commit()
                                print(Fore.GREEN + "\nPin updated successfully")
                                print(Fore.YELLOW + "\nPlease re-login again\n")
                                return
                    else:
                        print(Fore.RED + "Enter pin is in_correct Please Tryagain")
        elif ch=='4':#Credit into Account
            while True:
                new_amount=input("\nEnter Amount to credit in to account:")
                if not new_amount.isdigit():
                    print(Fore.RED + "Please Enter amount in digit_formate only")
                    continue
                else:
                    new_amount=int(new_amount)
                    if new_amount<=0:
                        print(Fore.RED + "Select Valid amount")
                    else:
                        
                        cur.execute('select amount from users where account_number=%s',(account_number,))
                        current_amount=cur.fetchone()
                        for curr_amo in current_amount:
                            cur.execute('Update users set amount=%s where account_number=%s',(curr_amo+new_amount,account_number))
                            now=dt.now()
                            tx_cid='TXN'+now.strftime('%Y%m%d%H%M%S')
                            res=amount(account_number)
                            cur.execute('insert into Transactions (transaction_id,Account_number,Transaction_type,Transaction_amount,Available_amount)values(%s,%s,%s,%s,%s)',\
                                (tx_cid,account_number,'CREDIT',new_amount,(res)))
                            con.commit()
                            print(Fore.GREEN + "\nAmount credited successfully into your bank account")
                            res=amount(account_number)
                            print(Fore.LIGHTCYAN_EX + "\nCurrent balance is:",res)
                        break
                    
        elif ch=='5':#Debit from Account
            while True:
                debit_amount=input("\nEnter amount to debit:")
                if not debit_amount.isdigit():
                    print(Fore.RED + "Please Enter amount in digit_formate only")
                    continue
                else:
                    debit_amount=int(debit_amount)
                    if debit_amount<=0:
                        print(Fore.RED + "Enter valid Amount")
                    else:
                        cur.execute('select amount from users where account_number=%s',(account_number,))
                        cur_bal=cur.fetchone()[0]
                        if cur_bal>debit_amount:
                            cur.execute('update users set amount=%s where account_number=%s',(cur_bal-debit_amount,account_number))
                            now=dt.now()
                            tx_did='TXN'+now.strftime('%Y%m%d%H%M%S')
                            res=amount(account_number)
                            cur.execute('insert into Transactions (transaction_id,Account_number,Transaction_type,Transaction_amount,Available_amount)values(%s,%s,%s,%s,%s)',\
                                (tx_did,account_number,'DEBIT',debit_amount,(res)))
                            con.commit()
                            print(Fore.GREEN + "\nAmount Debited Succesfully")
                            res=amount(account_number)
                            print(Fore.YELLOW + "Current Balance in your account is:",res)
                            break
                        else:
                            cur.execute('select amount from users where account_number=%s',(account_number,))
                            amo=cur.fetchone()[0]
                            print(Fore.LIGHTCYAN_EX + "The Expected amount is not in your Bank Account")
                            print(Fore.LIGHTMAGENTA_EX + "Current account balance is:",amo)
                            continue
                    
        elif ch=='6':#statement
            while True:
                print(Fore.GREEN + """
============================================
        1:Entire Transaction
        2:Paticular Date
        3.Transactions Between Date
        4:exit
============================================
                          """)
                ch=input("Enter choice: ")
                if ch=='1':
                    cur.execute("Select * from transactions where account_number=%s order by Transaction_time",(account_number,))
                    data=cur.fetchall()
                    headers=[desc[0] for desc in cur.description]
                    if data:
                        print(tb(data,headers=headers,tablefmt='fancy_grid'))
                elif ch=='2':
                    while True:
                        try:
                            date = input("Enter date of transactions (YYYY-MM-DD): ")
                            
                            # Validate date format in Python before sending to DB
                            try:
                                dt.strptime(date, "%Y-%m-%d")
                            except ValueError:
                                print(Fore.RED + "Invalid date format! Please enter in YYYY-MM-DD format.")
                                continue

                            cur.execute('select * from transactions WHERE account_number=%s and date(Transaction_time) = %s ', (account_number,date))
                            data = cur.fetchall()
                            headers = [desc[0] for desc in cur.description]

                            if data:
                                print(tb(data, headers=headers, tablefmt='fancy_grid'))
                                break
                            else:
                                print(Fore.CYAN + "No transactions happened on that date")
                                break
                        except :
                                print("Db Error")
                elif ch=='3':
                    statement(account_number)
                    '''while True:
                        try:
                            From_date=input("Enter From date of transactions (YYYY-MM-DD): ")
                            To_date=input("Enter  To date of transactions (YYYY-MM-DD): ")
                            try:
                                dt.strptime(From_date, "%Y-%m-%d")
                                dt.strptime(To_date, "%Y-%m-%d")
                            except ValueError:
                                print("\nInvalid date format! Please enter in YYYY-MM-DD format.")
                                continue
                            cur.execute('select * from transactions Where account_number=%s and date(Transaction_time)>=%s and date(transaction_time)<=%s',\
                                        (account_number,From_date,To_date))
                            data=cur.fetchall()
                            headers=[desc[0] for desc in cur.description]
                            if data:
                                print(tb(data,headers=headers,tablefmt='fancy_grid'))
                                break
                            else:
                                print("\nNo transactions Happend on that date")
                                break
                        except:
                            print("Db Error")'''
                elif ch=='4':
                    break
                else:
                    print(Fore.RED + "Invalid Option")

                
        elif ch=='7':#Tarnsfer with in our bank
            while True:
                transfer_account_number=input("\nEnter Transfer_account_number:")
                if (not transfer_account_number.isdigit()) or (len(transfer_account_number)!=14):
                    print(Fore.RED + "Invalid account_number contains 14 digits and be in digits only")
                else:
                    transfer_account_number=int(transfer_account_number)
                    if transfer_account_number==account_number:
                        print(Fore.YELLOW + "Its your account boss")
                        continue
                    cur.execute('select * from users where account_number=%s',(transfer_account_number,))
                    acc_no=cur.fetchone()
                    if acc_no==None:
                        print(Fore.RED + "Account_number Doesn't Exists Please check once\n")
                    else:
                        print(Fore.GREEN +"User name:",acc_no[0])
                        it=acc_no[1]
                        if it:
                            while True:
                                transfer_amount=input("\nEnter amount to Transfer:")
                                if not transfer_amount.isdigit():
                                    print(Fore.RED + "Invalid please check and enter only digits")
                                else:
                                    transfer_amount=int(transfer_amount)
                                    if transfer_amount<=0:
                                        print(Fore.RED + "Invalid amount")
                                        continue
                                    res=amount(account_number)
                                    if transfer_amount > res:
                                        print(Fore.LIGHTRED_EX + "Insufficient balance.",Fore. YELLOW + "Current balance is",res)
                                        continue
                                    cur.execute('update users set amount=%s where account_number=%s',((res-transfer_amount),account_number))
                                    con.commit()
                                    print(Fore.GREEN + "Amount Transfer Succesfully")
                                    now=dt.now()
                                    tx_tdid='TXNT'+now.strftime('%Y%m%d%M%S%H')
                                    res=amount(account_number)
                                    cur.execute('insert into transactions(Transaction_id,Account_number,Transaction_type,Transaction_amount,Available_Amount)\
                                    values(%s,%s,%s,%s,%s)',(tx_tdid,account_number,'DEBIT_TNF',transfer_amount,(res)))
                                    con.commit()
                                    res=amount(transfer_account_number)
                                    cur.execute('update users set amount=%s where account_number=%s',((res+transfer_amount),transfer_account_number))
                                    con.commit()
                                    now=dt.now()
                                    tx_tcid='TXNT'+now.strftime('%Y%m%d%H%M%S')
                                    res=amount(transfer_account_number)
                                    cur.execute('insert into transactions(Transaction_id,Account_number,Transaction_type,Transaction_amount,Available_amount)\
                                    values(%s,%s,%s,%s,%s)',(tx_tcid,transfer_account_number,'CREDIT_TNF',transfer_amount,(res)))
                                    con.commit()
                                    
                                    break
                    break
        
                    
        elif ch=='8':#logout
            print(Fore.YELLOW + "Thank you Visit again Have a nice day")
            return
        else:
            print(Fore.RED + "\nSelect valid Option")
def admin():#admin login
    while True:
        Admin_id=input("\nEnter Admin id:")
        if not Admin_id.isdigit():
            print(Fore.RED + "Check Your admin_id")
            continue
        else:
            Admin_id=int(Admin_id)
            cur.execute('select * from admin where Admin_id=%s',(Admin_id,))
            data=cur.fetchone()
            if data:
                print(Fore.GREEN + "Admin Found:",data[1])
            else:
                print(Fore.YELLOW + "Admin Not found")
                continue
            c=3
            while c>0:
                password=input("Enter password:")
                if len(password)!=4 or not password.isdigit():
                    print(Fore.RED + "Please enter valid pin\n")
                    c-=1
                    print(f"Attempts left {c}")
                    continue
                cur.execute("Select * from admin where Admin_id=%s and password=%s",(Admin_id,password))
                data=cur.fetchone()
                if data:
                    print(Fore.GREEN + f"welcome {data[1]}")
                    admin_operations()
                    return
    
                else:
                    print("\nInvalid admin credentials\n")
                    c-=1
                    print(f"\nAttempts left {c}\n")
            print("\nToo many attempts")
            break
                    
def admin_operations():#admin actions
    while True:
        print(Fore.GREEN + """
==============admin actions==============
        1:view all users
        2:view single user
        3:Transactions of particular user
        4:Complete transactions on particualar day
        5:Transactions Between Date
        6:logout
=========================================
            """)
        ch=input("Enter choice:")
        if not ch.isdigit():
            print(Fore.RED + "please choose corret choice")
        elif ch=='1':#view all user details in bank
              cur.execute('select User_Name,account_number,account_type,amount,Created_at from users')
              data=cur.fetchall()
              headers=['user_name','account_number','account_type','amount','Created_at']
              if data:
                  print(tb(data,headers=headers,tablefmt='fancy_grid'))
        elif ch=='2':#
            while True:
                acc_no=input("Enter account_number of holder:")
                if (not acc_no.isdigit()) or (len(acc_no)!=14):
                    print(Fore.RED + "Invalid account_number entry or must be in digits only")
                else:
                    acc_no=int(acc_no)
                    cur.execute('select User_Name,account_number,account_type,amount,Created_at from users where account_number=%s',(acc_no,))
                    data=cur.fetchone()
                    headers=['user_name','account_number','account_type','amount','Created_at']
                    if data:
                        print(tb([data],headers=headers,tablefmt='fancy_grid'))
                        break
                    else:
                        print(Fore.YELLOW + "NO user found please check")
                        break
        elif ch=='3':
            while True:
                acc_no=input("Enter account_number of holder:")
                if (not acc_no.isdigit()) or len(acc_no)!=14:
                    print(Fore.RED + "Invalid account_number")
                    continue
                acc_no=int(acc_no)
                cur.execute('select * from transactions where account_number=%s order by transaction_time',(acc_no,))
                data=cur.fetchall()
                headers=[desc[0] for desc in cur.description]
                if data:
                    print(tb(data,headers=headers,tablefmt='fancy_grid'))
                    break
                else:
                    print(Fore.LIGHTMAGENTA_EX + "Account_Not Found Please check")
                    break
        elif ch=='4':
            while True:
                print("""
======================================
        1:all users Transactions
        2:particular user transactions
        3:exit
=====================================
            """)
                choice=input("Enter transaction choice:")
                if not choice.isdigit():
                    print(Fore.RED + "Invalid Option Choose correct one")
                    continue
                if choice == '1':
                    while True:
                        try:
                            date = input("Enter date of transactions (YYYY-MM-DD): ")
                            
                            # Validate date format in Python before sending to DB
                            try:
                                dt.strptime(date, "%Y-%m-%d")
                            except ValueError:
                                print(Fore.RED + "Invalid date format! Please enter in YYYY-MM-DD format.")
                                continue

                            cur.execute('select * from transactions WHERE date(Transaction_time) = %s order by Transaction_time', (date,))
                            data = cur.fetchall()
                            headers = [desc[0] for desc in cur.description]

                            if data:
                                print(tb(data, headers=headers, tablefmt='fancy_grid'))
                                break
                            else:
                                print(Fore.YELLOW + "No transactions happened on that date")
                                break
                        except :
                                print("Db Error")
                elif choice=='2':
                    while True:
                        acc_no=input("Enter account_number:")
                        if not acc_no.isdigit():
                            print(Fore.RED + "Invalid account_number")
                        elif len(acc_no)!=14:
                            print(Fore.RED + "Account_number must be 14 digits only")
                        else:
                            acc_no=int(acc_no)
                            cur.execute('select * from users where account_number=%s',(acc_no,))
                            data=cur.fetchone()
                            if data:
                                print("User found:",data[0])
                                break
                            else:
                                print(Fore.LIGHTMAGENTA_EX + "User not Found")
                    while True:
                        try:
                            date=input("Enter date of transactions(YYYY-MM-DD): ")
                            try:
                                dt.strptime(date,"%Y-%m-%d")
                            except ValueError:
                                print(Fore.RED + "Invalid date format! Please enter in YYYY-MM-DD format.")
                                continue
                            cur.execute('select * from transactions where account_number=%s and DATE(Transaction_time)=%s',(acc_no,date))
                            data=cur.fetchall()
                            headers=[desc[0] for desc in cur.description]
                            if data:
                                print(tb(data,headers=headers,tablefmt='fancy_grid'))
                                break
                            else:
                                print(Fore.LIGHTMAGENTA_EX + "No transactions happend on that day")
                                break
                        except:
                            print("DB ERROR")
                elif choice=='3':
                    break
                else:
                    print(Fore.RED + "Choose Right option")
        elif ch=='5':#Between date range
            print("""
            1.All users
            2:Particular User
            3:Exit
            """)
            while True:
                cho=input("\nEnter choice for statement:")
                if cho=='1':
                    while True:
                        try:
                            from_date=input("Enter From date of transactions (YYYY-MM-DD): ")
                            to_date=input("Enter  To date of transactions (YYYY-MM-DD): ")
                            try:
                                dt.strptime(from_date, "%Y-%m-%d")
                                dt.strptime(to_date, "%Y-%m-%d")
                            except ValueError:
                                print(Fore.RED + "Invalid date format! Please enter in YYYY-MM-DD format.")
                                continue
                            cur.execute('select * from transactions Where date(transaction_time)>=%s and date(transaction_time)<=%s order by transaction_time',\
				    (from_date,to_date))
                            data=cur.fetchall()
                            headers=[desc[0] for desc in cur.description]
                            if data:
                                print(tb(data,headers=headers,tablefmt='fancy_grid'))
                                break
                            else:
                                print(Fore.YELLOW + "No transactions Happend on that date")
                            break
                        except:
                            print("Db Error")

                elif cho=='2':
                    while True:
                        acc_no=input("\nEnter account_number:")
                        if (not acc_no.isdigit()) or (len(acc_no)!=14):
                            print(Fore.RED + "Invalid account_number must be 14 digits only")
                        acc_no=int(acc_no)
                        cur.execute('select * from users where account_number=%s',(acc_no,))
                        data=cur.fetchone()
                        if data:
                            print(Fore.GREEN + "\nUser Found:",data[0])
                        else:
                            print(Fore.LIGHTMAGENTA_EX + "User Not found")
                            break
                        statement(acc_no)
                        break
                elif cho=='3':
                    break
                else:
                    print(Fore.RED + "Choose correct option")
        elif ch=='6':
            return
        else:
            print(Fore.RED + "_select valid choice_")
              
def main():
    while True:
        print(Fore.GREEN + """
==========Welcome==========
        1.User_login
        2.user_registration
        3.Admin_login
        4.exit
===========================
              """)
 
        try:
            choice=int(input("Please enter your choice: "))
        except ValueError:
            print(Fore.RED + "Please Choose correct option")
            continue
        if choice==1:
            user_login()
        elif choice==2:
            user_registration()
        elif choice==3:
            admin()
        elif choice==4:
            print(Fore.LIGHTBLUE_EX + "Thank you Visit again")
            return
        else:
            print(Fore.RED + "\n-------please select valid option-------")
#main()#main function calling
if __name__ == "__main__":
        main()
        cur.close()
        con.close()