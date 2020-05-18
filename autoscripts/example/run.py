"""run some things
"""

import argparse
import json
import pickle
import os
import time


if __name__ == '__main__':

    # load configuration
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--location", help="location of config file", type=str)
    args = parser.parse_args()
    with open(args.location, 'rb') as f:
        data = pickle.load(f)
        print('data was loaded')

    # perform tasks
    for i in range(10):
        time.sleep(3)
        print(f'loop{i}')
    print(os.getcwd())
    print('this is not a unique message.')

    # save output as indicated in the config.json file
    with open('output.json', 'w') as f:
        json.dump({'not_so_empty':'never'}, f)
    print('data successfully dumped from autoscript')
