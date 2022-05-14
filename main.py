import hashlib
import random
import os

RANDOM_LEN = 16

def inject(bs):
    # bytes to hex and reverse
    hex = bs.hex()[::-1]
    # hex to bytes
    bs = bytes.fromhex(hex)

    # random bytes
    b1 = os.urandom(RANDOM_LEN)
    b2 = os.urandom(RANDOM_LEN)
    bs = b1 + bs + b2
    
    return bs

def remove_inject(bs):
    bs = bs[RANDOM_LEN:-RANDOM_LEN]

    # bytes to hex and reverse
    hex = bs.hex()[::-1]

    # hex to bytes
    return bytes.fromhex(hex)

''' usage:
    py main.py -f sample.txt -i
    py main.py -f sample.txt -r
'''
if __name__ == '__main__':
    # parse args
    import argparse
    parser = argparse.ArgumentParser(description='choose one action with -i or -r')
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-i', '--inject', action='store_true')
    parser.add_argument('-r', '--remove', action='store_true')
    args = parser.parse_args()

    if not args.inject and not args.remove:
        parser.print_help()
        exit(1)

    # read binary file
    with open(args.file, 'rb') as f:
        bs = f.read()
    
    if args.inject:
        bs = inject(bs)
    elif args.remove:
        bs = remove_inject(bs)
    else:
        raise Exception('unknown action')

    # write binary file
    with open(args.file, 'wb') as f:
        f.write(bs)

    