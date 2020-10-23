#!/usr/bin/env python3

import os
import os.path
import sys
import struct
import argparse
import json

from util import check_challenge

from Cryptodome.Cipher import AES

import lfsr
LFSR_LEN = 64
LFSR_TAPS = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0,
             1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]


def bitsToBytes(bit_array):
    assert len(bit_array) % 8 == 0, "only accept full bytes"
    for x in bit_array:
        assert x in (0, 1), "input not a bit array"
    res = []
    for i in range(0, len(bit_array), 8):
        byte = 0
        for j in range(8):
            byte |= bit_array[i+j] << (7-j)
        res.append(byte)

    return bytearray(res)


def bytesToBits(byte_array):
    res = []
    for x in byte_array:
        for j in range(8):
            bit = (x >> (7-j)) & 1
            res.append(bit)
    return res


def writeConfig(config):
    config["key"] = config["key"].hex()
    with open('key_config', 'w') as f:
        json.dump(config, f)


def readConfig():
    with open('key_config', 'rb') as f:
        config = json.load(f)
    config["key"] = bytes.fromhex(config["key"])
    return config

# implementation of the XKCD random number generator (https://xkcd.com/221/)


def getRandomNumber():
    return 4  # chosen by a fair dice roll, guaranteed to be random
    # RFC 1149.5 specifies 4 as the standard IEEE-vetted random number.


def getRandomNonce():
    r = getRandomNumber()
    return r.to_bytes(8, byteorder='little')


def openCar(config):
    nonce = getRandomNonce()
    cipher = AES.new(key=config["key"], mode=AES.MODE_CTR, nonce=nonce)

    l = lfsr.LFSR(LFSR_LEN, config["state"], LFSR_TAPS)
    car_code = l.output(LFSR_LEN)
    car_code = bitsToBytes(car_code)
    config["index"] += 1
    config["state"] = l.state

    ct = cipher.encrypt(car_code)
    fname = config["name"] + "." + str(config["index"]) + ".enc"

    # write the car unlock code
    with open(fname, 'wb') as f:
        f.write(nonce)
        f.write(ct)

    # write back updated state to config file
    writeConfig(config)

########################################################################
# also part of our code

def touple_list(first, second):
    return [(first[i], second[i]) for i in range(len(first))]

def solve_challenge(challenge_fnames, solution_fname):
    challenge_files = challenge_fnames.split(",")
    nonces = []
    cts = []
    for filename in challenge_files:
        with open(filename, 'rb') as f:
            nonces.append(f.read(8))
            cts.append(f.read(8))

    next_nonce = bytes()
    next_ct = bytes()
########################################################################
# enter your code here

    # XOR 64 bits
    # reference: https://nitratine.net/blog/post/xor-python-byte-strings/
    state = bytesToBits([_ct1 ^ _ct0 for _ct1, _ct0 in touple_list(cts[1], cts[0])])
    
    # same as part in open car since we have to make a 
    # prediciton based on receiving device near car
    l = lfsr.LFSR(LFSR_LEN, state, LFSR_TAPS)
    l.output(LFSR_LEN)
    l.state = bitsToBytes(l.state)

    # find next_nonce same as part in open car since
    # it has to be random
    next_nonce = bytes(getRandomNonce())
    
    # find next_ct
    next_ct = bytes([_ct1 ^ _ct0 for _ct1, _ct0 in touple_list(cts[1], l.state)])

########################################################################

    with open(solution_fname, 'wb') as f:
        f.write(next_nonce)
        f.write(next_ct)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', title='command')
    subparsers.required = True
    parser_d = subparsers.add_parser('o', help='create car unlocking code')
    parser_g = subparsers.add_parser('g', help='keygen')
    parser_c = subparsers.add_parser('c', help='challenge')
    parser_c.add_argument('challenge_files', nargs='?', default='challenge.1.enc,challenge.2.enc',
                          help='default: challenge.1.enc,challenge.2.enc')
    parser_c.add_argument('output_file', nargs='?',
                          default='challenge.3.enc', help='default: challenge.3.enc')
    args = parser.parse_args()

    if args.command == 'g':
        key = os.urandom(16)
        lfsr_state = bytesToBits(os.urandom(LFSR_LEN//8))
        config = {
            "name": "car",
            "key": key,
            "state": lfsr_state,
            "index": 0,
        }
        writeConfig(config)
        return

    if args.command == 'o':
        if not os.path.isfile('key_config'):
            print('no key_config found, run key generation first')
            return -1
        else:
            config = readConfig()

        openCar(config)

    if args.command == 'c':
        solve_challenge(args.challenge_files, args.output_file)
        check_challenge(args.output_file)

        return


if __name__ == "__main__":
    sys.exit(main())

