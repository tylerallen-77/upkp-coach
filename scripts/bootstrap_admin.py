from __future__ import annotations
import argparse,getpass,sys
from argon2 import PasswordHasher
from upkp import multi_store as store

def main():
    ap=argparse.ArgumentParser(description='Create or promote the reserved UPKP Coach admin safely.')
    ap.add_argument('--username',required=True)
    args=ap.parse_args();username=args.username.strip().lower()
    if not store.DATABASE_URL:
        raise SystemExit('DATABASE_URL must point to the production Supabase database.')
    existing=store.get_user_by_username(username)
    if existing:
        print(f'User @{username} exists. Promoting existing account only if this is yours.')
        confirm=input('Type PROMOTE to continue: ')
        if confirm!='PROMOTE':raise SystemExit('Cancelled')
        store.set_role(existing['id'],'admin');print('Admin role granted.');return
    p1=getpass.getpass('Admin password (min 12 chars recommended): ')
    p2=getpass.getpass('Repeat password: ')
    if p1!=p2 or len(p1)<8:raise SystemExit('Passwords mismatch or too short.')
    ph=PasswordHasher(time_cost=2,memory_cost=19456,parallelism=1)
    u=store.create_user(username,ph.hash(p1),'admin')
    print(f'Created admin @{u["username"]}.')
if __name__=='__main__':main()
