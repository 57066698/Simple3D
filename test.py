## expNet npz

import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np

x = tf.Variable(np.ones((1, 2)), dtype=tf.float32)
w = tf.Variable(np.ones((2, 2)), dtype=tf.float32)
y = tf.Variable(np.ones((1, 2)) * 3, dtype=tf.float32)

def loss(w_1d):
    w = tf.reshape(w_1d, (2, 2))
    return tf.reduce_sum(tf.square(tf.matmul(x, w) - y))

def quadratic(w_1d):
    return tfp.math.value_and_gradient(loss, w_1d)

w_1d = tf.reshape(w, -1)

optim_results = tfp.optimizer.lbfgs_minimize(quadratic, initial_position=w_1d)
print(optim_results.position)