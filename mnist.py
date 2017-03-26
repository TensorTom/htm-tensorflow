import tensorflow as tf
import numpy as np
from util import *
from math import *
from layers.spatial_pooler import SpatialPoolingLayer

import matplotlib.pyplot as plt

epochs = 10
dim = [784, 10]
sparsity = 0.02
learning_rate = 0.1

def build_model():
    # Model input
    x = tf.placeholder(tf.bool, [1, dim[0]], name='Input')
    y = SpatialPoolingLayer(1024)(x)
    return y

def main():
    # Build a model
    model = build_model()

    # Load MNSIT
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets("data/", one_hot=False)

    # Process data
    input_set = [[x] for x in mnist.train.images[:10000]]

    with tf.Session() as sess:
        # Run the 'init' op
        sess.run(tf.global_variables.initializer())


        for epoch in range(epochs):
            print('===     Epoch ' + str(epoch) + '     ===')
            for i, x in enumerate(input_set):
                sess.run([layer.y, layer.learn], feed_dict={layer.x: x})
                progress_bar(i / float(len(input_set)))
            print()

            print(' == Clustering ==')
            """
            Take all the inputs and determine its cluster based on
            average values.
            """
            counts = [0 for _ in range(dim[1])]
            clusters = [0 for _ in range(dim[1])]

            for input, label in zip(input_set, mnist.train.labels):
                clusters[label] += sess.run(layer.y, feed_dict={layer.x: input})
                counts[label] += 1

            for c in range(len(clusters)):
                clusters[c] /= counts[c]

            print(sess.run(layer.p))
            print(clusters[0])
            print(clusters[1])

            print(' == Validating == ')

            correct = 0
            for input, c in zip(mnist.validation.images, mnist.validation.labels):
                # Find best match in cluster
                best_class = None
                min_norm = inf
                output = sess.run(layer.y, feed_dict={layer.x: [input]})
                for k, cluster in enumerate(clusters):
                    diff = np.linalg.norm(cluster - output)
                    if diff < min_norm:
                        min_norm = diff
                        best_class = k

                # Validate if best class is correct
                if c == best_class:
                    correct += 1

            print('Accuracy: ', correct / float(len(mnist.validation.images)))