import argparse

from tinder.tinder_controller import TinderController
from tinder.conversations.app import app
from tinder.decision_making.model import Model


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-d', dest='d', action='store_true', help='to run in dataset collection mode')
    # parser.add_argument('-f', '--folder', dest='f', default='dataset', help='where to store data in dataset collection mode')
    # args = parser.parse_args()
    #
    # controller = TinderController()
    # if args.d:
    #     controller.start_dataset_collecting(args.f)
    # else:
    #     # auto-mode
    #     pass
    # # app.run()
    model = Model()
    model.split_data('dataset')
    model.define_model()