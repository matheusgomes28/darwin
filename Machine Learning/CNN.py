from __future__ import division, print_function, absolute_import
import tensorflow as tf
import CNN
# from Predictions import Predictions


class CNN:
    # Define CNN layers in this function (current stuff is just temporary to test it works...)
    def conv_net(self, features, reuse, is_training):
        with tf.variable_scope('conv', reuse=reuse) as scope:
            x = features['images']

            # 784 images in MNIST
            # [batch size, height, width, channel]
            x = tf.reshape(x, shape=[1, 64, 64, 1])

            # Convolution Layer with 32 filters and a kernel size of 13
            conv1 = tf.layers.conv2d(x, 32, 7, activation=tf.nn.relu, name='conv1')

            # First pooling layer
            pool1 = tf.layers.max_pooling2d(conv1, 2, 2, name='pool1')

            # Convolution Layer with 64 filters and a kernel size of 3
            conv2 = tf.layers.conv2d(pool1, 64, 5, activation=tf.nn.relu, name='conv2')

            # Second pooling layer
            pool2 = tf.layers.max_pooling2d(conv2, 2, 2, name='pool2')

            # Flatten the data to a 1-D vector for the fully connected layer
            flatten = tf.contrib.layers.flatten(pool2)

            # Fully connected layer (in tf contrib folder for now)
            fully_connected = tf.layers.dense(flatten, 1024)
            fully_connected = tf.layers.dropout(fully_connected, rate=self.dropout, training=is_training)

            # Output layer, class prediction
            out = tf.layers.dense(fully_connected, self.num_classes)

        return out

    def train_conv_net(self, features):
        return self.conv_net(features, False, True)

    def test_conv_net(self, features):
        return self.conv_net(features, True, False)

    def model_fn(self, features, labels, mode):
        train_logits = self.train_conv_net(features)
        test_logits = self.test_conv_net(features)

        # Predictions stored in a wrapper class
        predictions = Predictions(test_logits)

        # If currently making predictions with the model, exit early
        if mode == tf.estimator.ModeKeys.PREDICT:
            return tf.estimator.EstimatorSpec(mode, predictions=predictions.classes)

        # Loss function
        loss_fn = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=train_logits,
                                                                                labels=tf.cast(labels, dtype=tf.int32)))

        # Optimiser
        optimiser = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        train_optimiser = optimiser.minimize(loss_fn, global_step=tf.train.get_global_step())

        # Model accuracy
        accuracy = tf.metrics.accuracy(labels=labels, predictions=predictions.classes)

        estimator_spec = tf.estimator.EstimatorSpec(mode=mode,
                                                    predictions=predictions.classes,
                                                    loss=loss_fn,
                                                    train_op=train_optimiser,
                                                    eval_metric_ops={'accuracy': accuracy})

        return estimator_spec

    def get_model(self):
        return tf.estimator.Estimator(self.model_fn)

    def __init__(self, learning_rate, num_classes, dropout):
        self.learning_rate = learning_rate
        self.num_classes = num_classes
        self.dropout = dropout
