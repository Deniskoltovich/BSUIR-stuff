from arsparser import args

from encryption import ImageEncrypter


if __name__ == '__main__':
    ImageEncrypter.encrypt_image(args.f, args.key,
                                 args.algo, args.mode)