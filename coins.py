'''flip coins, stop when losing all money'''

import random

def tosscoin():
    if random.random() < 1/2:
        return 0
    else:
        return 1
    
try:
    n = input('Enter your starting money:')
except ValueError:
    print('invalid input.')

balance = float(n)
tosses = 0
while balance > 0:
    tosses = tosses + 1
    if tosscoin() == 1:
        balance = balance + 1
        print('Heads! Current amount: {0:.1f}.'.format(balance))
    else:
        balance = balance - 1.5
        print('Tails! Current amount: {0:.1f}.'.format(balance))

print('Game over! Current amount: {0:.1f}. Coin tosses: {1:d}.'.format(balance, tosses))