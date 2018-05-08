import tensorflow as tf
import argparse
from CNN import CNN
from tensorflow.examples.tutorials.mnist import input_data


def main():
    # Data set specific globals (need changing for different data sets)
    NUM_CLASSES = 10
    DROPOUT = 0.25

    # Default values
    default_learning_rate = 0.001
    default_num_steps = 2000
    default_batch_size = 128

    # Command line parsing
    parser = argparse.ArgumentParser(description='Test CNN for classifying images.', conflict_handler='resolve')
    parser.add_argument('learning_rate', help='learning rate of the CNN', nargs='?', type=float,
                        default=default_learning_rate)
    parser.add_argument('num_steps', help='number of steps to take in the training stage', nargs='?', type=int,
                        default=default_num_steps)
    parser.add_argument('batch_size', help='CNN batch size (power of 2)', nargs='?', type=int,
                        default=default_batch_size)
    args = parser.parse_args()

    # Temporary MNIST data set (conveniently divided into training and testing)
    data = input_data.read_data_sets('/tmp/data/', one_hot=False)
    train_images = data.train.images
    train_labels = data.train.labels
    test_images = data.test.images
    test_labels = data.test.labels

    # Creating the training input function
    train_input = tf.estimator.inputs.numpy_input_fn(x={'images': train_images},
                                                     y=train_labels,
                                                     batch_size=args.batch_size,
                                                     num_epochs=None,
                                                     shuffle=True)

    # Creating the testing input functions
    test_input = tf.estimator.inputs.numpy_input_fn(x={'images': test_images},
                                                    y=test_labels,
                                                    batch_size=args.batch_size,
                                                    shuffle=False)

    # Creating the model
    cnn = CNN(args.learning_rate, NUM_CLASSES, DROPOUT)
    model = cnn.get_model()

    # Training
    model.train(train_input, steps=args.num_steps)

    # Evaluating
    # For each step, calls test_input which returns batch of data
    # Returns dict of eval_metric_ops
    evaluation = model.evaluate(test_input)
    print('Accuracy: {}'.format(evaluation['accuracy']))


if __name__ == '__main__':
    print('This takes a while...')
    main()
