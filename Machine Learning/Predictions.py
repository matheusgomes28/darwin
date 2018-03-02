import tensorflow as tf

class Predictions:

  def __init__(self, test_logits):
    self.classes = tf.argmax(test_logits, axis=1)
    self.probabilities = tf.nn.softmax(test_logits)
