import argparse

from tinder.tinder_controller import TinderController
from tinder.conversations.app import app
from tinder.decision_making.model import Model
from tinder.decision_making.test_model import make_test_prediction

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='d', action='store_true', help='to run in dataset collection mode')
    parser.add_argument('-f', '--folder', dest='f', default='dataset', help='where to store data in dataset collection mode')
    parser.add_argument('-s', dest='s', action='store_true', help='to run in swiping mode')
    args = parser.parse_args()

    controller = TinderController()
    if args.d:
        controller.start_dataset_collecting(args.f)
    elif args.s:
        # auto-mode
        controller.start_swiping()
    # app.run()
    # model = Model()
    # model.split_data('dataset')
    # model.define_model()

    # make_test_prediction('https://images-ssl.gotinder.com/5fabbc47877f260100eda5b5/640x800_75_fbfe8c74-02ea-4238-b4c3-5b23aef0da54.webp')
