import sqlite3


class banking_system:
    def __init__(self):
        self.conn = sqlite3.connect("bankdata.db")
        self.crsr = self.conn.cursor()
        self.crsr.execute('create table if not exists AccInfo (cust_id INTEGER PRIMARY KEY, name VARCHAR(20), acc_name VARCHAR(20), balance VARCHAR(20));')
        self.crsr.execute('SELECT * FROM AccInfo')
        try:
            self.ctr = self.crsr.fetchall()[-1][0]
        except:
            self.ctr = 0
    
    def create_acc(self, name, acc_name):
        self.crsr.execute(f'SELECT * FROM AccInfo WHERE name="{name}";')
        result = self.crsr.fetchone()
        if result == None:
            self.crsr.execute(f'INSERT INTO AccInfo VALUES ("{self.ctr+1}", "{name}", "{acc_name}", "{0}");')
            self.conn.commit()
            self.ctr += 1
        else:
            print(f'Account with number {name} already exists')
    
    def check_balance(self, acc_no):
        self.crsr.execute(f'SELECT balance,acc_name from AccInfo WHERE name ="{acc_no}";')
        details = self.crsr.fetchone()
        print(f'{details[1]} {int(float(details[0]))}')

    def withdraw(self, acc_no, amount):
        try:
            amount = float(amount)
        except:
            print('Invalid Amount')
        self.crsr.execute(f'SELECT balance from AccInfo WHERE name ="{acc_no}";')
        aval_balance = self.crsr.fetchone()
        if aval_balance == None:
            raise Exception('No Such Account Exists')
        aval_balance = float(aval_balance[0])
        if aval_balance - amount < 0:
            print('Cannot Complete Transaction : Insufficient Balance')
        else:
            upd_balance = aval_balance - amount
            self.crsr.execute(f'UPDATE AccInfo SET balance = "{upd_balance}" WHERE name="{acc_no}";')
            # print(f'updated balance : {upd_balance}')
        self.conn.commit()
    
    def deposit(self, acc_no, amount):
        try:
            amount = float(amount)
        except:
            print('Invalid Amount')
        self.crsr.execute(f'SELECT balance from AccInfo WHERE name ="{acc_no}";')
        try:
            aval_balance = float(self.crsr.fetchone()[0])
        except:
            print('Invalid Account Number')
        
        upd_balance = aval_balance + amount
        self.crsr.execute(f'UPDATE AccInfo SET balance = "{upd_balance}" WHERE name="{acc_no}";')
        self.conn.commit()
        # print(f'updated balance : {upd_balance}')
        



        
if __name__ == '__main__':
    a = banking_system()
    
    print('\t\twelcome to the banking system\n\t\t(press "q" for exit)\n')
    while True:
        cmd = input('command>>').upper()
        if cmd == 'Q':
            quit()
        cmd = cmd.split(' ')
        base_cmd = cmd[0]
        if base_cmd == 'CREATE':
            a.create_acc(cmd[1],cmd[2])
        elif base_cmd == 'DEPOSIT':
            a.deposit(cmd[1],cmd[2])
        elif base_cmd == 'WITHDRAW':
            a.withdraw(cmd[1], cmd[2])
        elif base_cmd == 'BALANCE':
            a.check_balance(cmd[1])
        else:
            print('Invalid Command')

