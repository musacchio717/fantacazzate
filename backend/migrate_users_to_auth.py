"""
Script di migrazione utenti da sistema vecchio a nuovo con username/password e ruoli.

Esegui una sola volta: python migrate_users_to_auth.py

Aggiunge username e role agli utenti esistenti.
Genera password nuove per i 4 admin (LUCA F, LUCA R, DAVIDE, CICCIO).
Preserva tutte le relazioni (cazzate, aste, ecc.).
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.services.user_service import UserService
from app.core.auth import hash_password
import random
import string

def generate_password(length=5):
    """Genera una password random di 5 caratteri (lettere e numeri)."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_unique_username(db, base, exclude_id=None):
    """Genera uno username unico."""
    username = base
    counter = 1
    
    while True:
        user = db.query(User).filter(User.username == username).first()
        if user is None or (exclude_id and user.id == exclude_id):
            return username
        username = f"{base}_{counter}"
        counter += 1

def main():
    # Usa il DB locale SQLite anziché Railway
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Crea una sessione locale SQLite
    engine = create_engine("sqlite:///./fantacazzate.db")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    print("\n" + "="*70)
    print("MIGRAZIONE UTENTI - Fantacazzate")
    print("="*70 + "\n")
    
    # Prendi tutti gli utenti ordinati per ID
    users = db.query(User).order_by(User.id).all()
    
    if not users:
        print("❌ Nessun utente trovato nel database.")
        print("   Esegui prima seed.py per creare gli utenti iniziali.")
        db.close()
        return
    
    print(f"Trovati {len(users)} utenti nel database.\n")
    
    migrated = []
    
    for user in users:
        print(f"Migrazione utente: {user.nickname}")
        
        # Genera username se non esiste
        if not user.username:
            base_username = user.nickname.lower().replace(" ", "_")
            user.username = generate_unique_username(db, base_username, user.id)
            print(f"  ✓ Username generato: {user.username}")
        else:
            print(f"  ✓ Username esistente: {user.username}")
        
        # Assegna ruolo admin se non esiste
        if not user.role:
            user.role = UserRole.ADMIN
            print(f"  ✓ Ruolo assegnato: admin")
        else:
            print(f"  ✓ Ruolo esistente: {user.role}")
        
        # Genera password nuova (sempre)
        password = generate_password(5)
        user.hashed_password = hash_password(password)
        print(f"  ✓ Password generata: {password}")
        
        migrated.append({
            "user_id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "password": password,
            "role": user.role
        })
        
        print()
    
    # Salva tutti i cambiamenti
    db.commit()
    
    print("="*70)
    print("MIGRAZIONE COMPLETATA!")
    print("="*70 + "\n")
    
    print("Credenziali finali:\n")
    for user in migrated:
        print(f"Username:  {user['username']}")
        print(f"Nickname:  {user['nickname']}")
        print(f"Password:  {user['password']}")
        print(f"Ruolo:     {user['role']}")
        print()
    
    # Salva su file per sicurezza
    with open("migrated_credentials.txt", "w") as f:
        f.write("CREDENZIALI MIGRATE - FANTACAZZATE\n")
        f.write("="*50 + "\n")
        f.write(f"Data migrazione: {datetime.now().isoformat()}\n\n")
        
        for user in migrated:
            f.write(f"Username:  {user['username']}\n")
            f.write(f"Nickname:  {user['nickname']}\n")
            f.write(f"Password:  {user['password']}\n")
            f.write(f"Ruolo:     {user['role']}\n")
            f.write("-"*50 + "\n")
    
    print(f"✓ Credenziali salvate anche in: migrated_credentials.txt")
    print("="*70 + "\n")
    
    db.close()

if __name__ == "__main__":
    main()