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

########################################################################
# also part of our code
# reference: https://stackoverflow.com/questions/10106901/elegant-find-sub-list-in-list

def subfinder(list, pattern):
    for i in range(len(list)):
        if list[i] == pattern[0] and list[i:i+len(pattern)] == pattern:
            return i+len(pattern)-1


def solve_challenge(blog_file, enc_file):
    with open(blog_file, 'r') as f:
        blog = f.read()

    with open(enc_file, 'rb') as f:
        enc = f.read()

    pw = ''

########################################################################
# enter your code here

    # make a list from blog
    blog_list = blog.split(" ")
    word_list = [] 
    for element in blog_list:
        word_length = len(element)
        word_list.append(word_length)

    # lenght of first and last element from the blog
    first_element = 0
    last_element = word_list[-1] 
    print(last_element)

    # find all spaces in a file
    idx_counter = 0
    space_list = []
    for character in blog:
        idx_counter += 1
        if character == " ":
            space_list.append(idx_counter)
    
    # every block has to have 16 bytes
    enc = [enc[y - 16:y] for y in range(16, len(enc) + 16, 16)]
    
    # beginning and end of the blog
    counter = 1
    for character in enc:
        trace = counter 
        idx_space_list = 0
        for space in space_list[1:-1]:
            if character == enc[space - space_list[idx_space_list] + trace - 1]:
                trace += (space - space_list[idx_space_list])
                idx_space_list += 1
            else:
                break
        
        # -1 for len and -1 for last element
        if idx_space_list == len(space_list) - 2: 
            first_element = counter - space_list[0] 
            end = last_element + trace
            break
       
        counter += 1
    
    # username: bruce
    bruce = []
    for character in enc[first_element:end]:
        bruce.append(character)
    
    character = ["b", "r", "u", "c", "e"]
    bruce_found = []
    for char in character:
        bruce_found = bruce_found + [bruce[blog.index(char)]]

    bruce_last_idx = subfinder(enc, bruce_found)

    pw_cypher = []
    for character in enc[bruce_last_idx:first_element]:
        pw_cypher.append(character)
    
    # end of the challenge
    pw = ''.join([blog[bruce.index(set)] for set in pw_cypher[1::]])
            
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

