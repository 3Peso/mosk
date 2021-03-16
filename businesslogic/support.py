import os


def get_userfolders():
    for f in os.scandir('/Users'):
        if f.is_dir():
            yield f
