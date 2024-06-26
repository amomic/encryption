#!/usr/bin/env python3

import os
import os.path
import random
import sys
import argparse
import math
import string

from util import check_challenge
from Cryptodome.PublicKey import RSA
from Cryptodome.Math.Numbers import Integer

pkfile = 'rsa_key.pub'
skfile = 'rsa_key'


def rsa_kg():
    key = RSA.generate(4096)

    with open(skfile, 'wb') as f:
        f.write(key.exportKey('PEM'))

    pk = key.publickey()

    with open(pkfile, 'wb') as f:
        f.write(pk.exportKey('PEM'))


def rsa_encrypt(fname):
    with open(pkfile, 'rb') as f:
        sk = RSA.importKey(f.read(), 'PEM')

    with open(fname, 'rb') as f:
        pt = f.read()
        pt = int.from_bytes(pt, byteorder="little")

    if pt > sk.n:
        print("Plaintext must be smaller than modulus to allow encryption!")
        sys.exit(-1)

    # Textbook RSA; Cryptodome.Cipher.PKCS1_OAEP for practical RSA (with padding)
    ct = pow(pt, sk.e, sk.n)

    nlen = sk.size_in_bytes()
    ct = ct.to_bytes(nlen, byteorder="little")

    with open(fname + '.enc', 'wb') as f:
        f.write(ct)


def rsa_decrypt(fname):
    with open(skfile, 'rb') as f:
        sk = RSA.importKey(f.read(), 'PEM')

    with open(fname + '.enc', 'rb') as f:
        ct = f.read()
        ct = int.from_bytes(ct, byteorder="little")

    if ct > sk.n:
        print("Ciphertext is invalid (larger than modulus)!")
        sys.exit(-1)

    pt = pow(ct, sk.d, sk.n)
    ptlen = math.ceil(pt.bit_length() / 8)
    pt = pt.to_bytes(ptlen, byteorder="little")

    with open(fname, 'wb') as f:
        f.write(pt)


def solve_challenge(fname):
    with open(fname + '.enc', 'rb') as f:
        ct = f.read()

    with open(pkfile, 'rb') as f:
        pk = RSA.importKey(f.read(), 'PEM')

    pt = bytes()
########################################################################
# enter your code here

    def possible_cominations():
        combinations = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for first in alphabet:
            for second in alphabet:
                for third in alphabet:
                    combination = first + second + third
                    message = "Congratulations! Your flight destination is: " + combination
                    combinations.append(message)

        return combinations

    def combinations():
        combinations = possible_cominations()
        for combination in combinations:
            x = combination.encode()
            text = int.from_bytes(x, byteorder="little")
            text = pow(text, pk.e, pk.n)
            text = text.to_bytes(pk.size_in_bytes(), byteorder="little")

            if ct == text:
                pt = combination.encode()
                break;
        return pt

    pt = combinations()

    ########################################################################
    with open(fname, 'wb') as f:
        f.write(pt)
        return


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', title='subcommand')
    subparsers.required = True
    parser_e = subparsers.add_parser('e', help='encrypt')
    parser_e.add_argument('file')
    parser_d = subparsers.add_parser('d', help='decrypt')
    parser_d.add_argument('file')
    parser_g = subparsers.add_parser('g', help='keygen')
    parser_c = subparsers.add_parser('c', help='challenge')
    parser_c.add_argument(
        'file',
        nargs='?',
        default='challenge.enc',
        help='default: challenge.enc')
    args = parser.parse_args()

    if args.command == 'g':
        rsa_kg()
        return

    fname = args.file
    if not os.path.isfile(fname):
        print('no valid file specified')
        return -1

    if args.command == 'e':
        if not (os.path.isfile(pkfile)):
            print('no public key found, run key generation first!')
            return -1
        rsa_encrypt(fname)
        return

    if args.command == 'd':
        if not (os.path.isfile(pkfile)):
            print('no private key found, run key generation first!')
            return -1
        rsa_decrypt(fname[:-4])
        return

    if args.command == 'c':
        if not (os.path.isfile(pkfile)):
            print('no public key found, restore original public key first!')
            return -1
        solve_challenge(fname[:-4])
        check_challenge(fname[:-4])
        return


if __name__ == "__main__":
    sys.exit(main())
