import os

ROOT_DIR_PATH = os.path.split(os.path.realpath(__file__))[0]
MAX_MEAN_VALUE = 1e5
MAX_STD_VALUE = 1e6

ENROLL_FEATURE_PATH = os.path.join(ROOT_DIR_PATH, './feature')
SCORE_PATH = os.path.join(ROOT_DIR_PATH, './score')

THRESHOLD = -0.620026

if __name__ == '__main__':
    print(ROOT_DIR_PATH)
