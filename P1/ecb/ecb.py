#!/usr/bin/env python3

import os
import os.path
import sys
import argparse

from util import check_challenge

from Cryptodome.Cipher import AES


def enc_text(fname, key):
    cipher = AES.new(key=key, mode=AES.MODE_ECB)

    pt = open(fname, 'r')

    # we want to emulate keyboard input --> send each byte separately
    ct = open(fname + '.enc', 'wb')
    while True:
        p = pt.read(1)
        if p == '':
            break
        p = bytes(p, 'ascii') + bytes(15)
        ct.write(cipher.encrypt(p))

    pt.close()
    ct.close()


def dec_text(fname, key):
    cipher = AES.new(key=key, mode=AES.MODE_ECB)

    ct = open(fname + '.enc', 'rb')
    pt = open(fname, 'w')

    while True:
        c = ct.read(16)
        if c == b'':
            break
        p = cipher.decrypt(c)
        p = p.decode('ascii')[0]
        pt.write(p)

    ct.close()
    pt.close()


def solve_challenge(blog_file, enc_file):
    with open(blog_file, 'r') as f:
        blog = f.read()

    with open(enc_file, 'rb') as f:
        enc = f.read()

    pw = ''
########################################################################
# enter your code here

########################################################################
    with open('password', 'w') as f:
        f.write(pw)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', title='command')
    subparsers.required = True
    parser_e = subparsers.add_parser('e', help='encrypt')
    parser_e.add_argument('file', nargs='+')
    parser_d = subparsers.add_parser('d', help='decrypt')
    parser_d.add_argument('file', nargs='+')
    parser_g = subparsers.add_parser('g', help='keygen')
    parser_c = subparsers.add_parser('c', help='challenge')
    parser_c.add_argument(
        'blog',
        nargs='?',
        default='blog',
        help='default: blog')
    parser_c.add_argument(
        'sniffed_stream',
        nargs='?',
        default='sniffed_stream.enc',
        help='default: sniffed_stream.enc')
    args = parser.parse_args()

    if args.command == 'g':
        key = os.urandom(16)
        with open('key', 'wb') as f:
            f.write(key)
        return

    if args.command == 'e' or args.command == 'd':
        if not os.path.isfile('key'):
            print('no key found, run key generation first')
            return -1
        else:
            with open('key', 'rb') as f:
                key = f.read()
            files = [
                t for t in args.file if (
                    os.path.isfile(t) and not t == 'key')]

    if args.command == 'e':
        # we don't encrypt already encrypted files
        files = [t for t in files if not t.endswith('.enc')]
        if len(files) == 0:
            print('No valid files selected')
            return

        for f in files:
            enc_text(f, key)

        return

    if args.command == 'd':
        # we only want encrypted files
        files = [t[:-4] for t in files if t.endswith('.enc')]
        if len(files) == 0:
            print('No valid files selected')
            return

        for f in files:
            dec_text(f, key)

        return

    if args.command == 'c':
        solve_challenge(args.blog, args.sniffed_stream)

        check_challenge('password')

        return


if __name__ == "__main__":
    sys.exit(main())
