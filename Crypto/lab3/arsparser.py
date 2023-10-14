import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str,
                    help='path to file')
parser.add_argument('--algo', type=str,
                    choices=['AES', 'DES'],
                    help='AES or DES algorithm')

parser.add_argument('--mode', type=str,
                    choices=['ECB', 'CBC', 'CFB', 'OFB', 'CTR'],
                    help="'ECB', 'CBC', 'CFB', 'OFB', 'CTR' modes")
parser.add_argument('--key', type=str,
                    default='1000000000000000',
                    help='Default 10000000 for DES and 1000000000000000 for AES')
args = parser.parse_args()

args.key = '10000000' if args.algo == 'DES' and args.key == '1000000000000000' else args.key
print(args.key)
