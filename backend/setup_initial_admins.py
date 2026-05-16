"""
Script per creare i 4 admin iniziali.
Esegui una sola volta: python setup_initial_admins.py

Genera le password random e le stampa a schermo.
"""

import os
import sys
from datetime import datetime

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.user_service import UserService

def main():
    db = SessionLocal()
    service = UserService(db)
    
    initial_admins = [
        {"nickname": "LUCA F", "username_base": "luca_f"},
        {"nickname": "LUCA R", "username_base": "luca_r"},
        {"nickname": "DAVIDE", "username_base": "davide"},
        {"nickname": "CICCIO", "username_base": "ciccio"},
    ]
    
    print("\n" + "="*70)
    print("SETUP ADMIN INIZIALI - Fantacazzate")
    print("="*70 + "\n")
    
    created_users = []
    
    for admin in initial_admins:
        result = service.create_user(
            nickname=admin["nickname"],
            role="admin"
        )
        created_users.append(result)
        
        print(f"✓ Admin creato:")
        print(f"  Nickname:  {result['nickname']}")
        print(f"  Username:  {result['username']}")
        print(f"  Password:  {result['password']}")
        print(f"  Role:      {result['role']}")
        print()
    
    print("="*70)
    print("SALVA QUESTE CREDENZIALI IN UN POSTO SICURO!")
    print("="*70 + "\n")
    
    # Stampa anche in formato CSV per facilità
    print("Formato CSV (username,password):")
    for user in created_users:
        print(f"{user['username']},{user['password']}")
    
    print("\n" + "="*70)
    print("Setup completato!")
    print("="*70 + "\n")
    
    db.close()

if __name__ == "__main__":
    main()