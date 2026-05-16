"""
Script per impostare le password dei 4 admin.
Uso: python set_passwords.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ["DATABASE_URL"] = "sqlite:///./fantacazzate.db"

from app.core.database import SessionLocal
from app.models.user import User
from app.core.auth import hash_password

def set_passwords():
    db = SessionLocal()
    
    print("\n" + "="*70)
    print("IMPOSTA PASSWORD ADMIN")
    print("="*70 + "\n")
    
    users = db.query(User).all()
    
    for user in users:
        print(f"Utente: {user.username} ({user.nickname})")
        password = input("  Inserisci password: ").strip()
        
        if not password:
            print("  ❌ Password vuota, skip.\n")
            continue
        
        user.hashed_password = hash_password(password)
        db.commit()
        print(f"  ✓ Password impostata!\n")
    
    print("="*70)
    print("Fatto!")
    print("="*70 + "\n")
    db.close()

if __name__ == "__main__":
    set_passwords()