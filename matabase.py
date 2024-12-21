import sqlite3
import datetime

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def setup_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0,
        last_claim_date TEXT DEFAULT '1970-01-01'
    )
    """)
    conn.commit()
    conn.close()

class UserAlreadyExistsError(Exception):
    """Kullanıcı zaten mevcut olduğunda fırlatılan özel hata."""
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"Kullanıcı {user_id} zaten kayıtlı."
        super().__init__(self.message)

def add_user(user_id, username):
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is not None:
        print(f"Kullanıcı {user_id} zaten kayıtlı.")
        raise UserAlreadyExistsError(user_id)
    else:
        cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()


def update_balance(user_id, amount):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE user_id = ?
    """, (amount, user_id))
    conn.commit()
    conn.close()

def get_user_balance(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT balance
    FROM users
    WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

import datetime

def change_balance(user_id, amount):
    # Kullanıcının mevcut bakiyesini ve son ödül tarihini al
    cursor.execute("SELECT balance, last_claim_date FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()
    
    if user_data is None:
        raise ValueError("Kullanıcı bulunamadı!")

    current_balance = user_data[0]
    last_claim_date = user_data[1]

    # Eğer kullanıcı daha önce hiç ödül almadıysa, last_claim_date None olabilir.
    if last_claim_date is None:
        last_claim_date = "1970-01-01"  # Eski bir tarih belirleyelim

    # Bugünün tarihini al
    today = datetime.datetime.today().date()

    # Kullanıcının son ödül aldığı tarihi datetime objesine çevir
    last_claim_datetime = datetime.datetime.strptime(last_claim_date, "%Y-%m-%d").date()

    # Eğer son ödül alınmasının üzerinden 1 gün geçmişse
    if (today - last_claim_datetime).days >= 1:
        # Yeni bakiyeyi hesapla
        new_balance = current_balance + amount

        # Yeni bakiyeyi veritabanına güncelle
        cursor.execute("UPDATE users SET balance=?, last_claim_date=? WHERE user_id=?", 
                       (new_balance, today, user_id))
        conn.commit()

        return new_balance
    else:
        raise ValueError("Henüz günlük ödülünüzü almadınız, bir sonraki gün tekrar deneyin!")
