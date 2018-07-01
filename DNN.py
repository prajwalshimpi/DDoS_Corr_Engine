from __future__ import absolute_import, division, print_function
import itertools
import pandas as pd
import os
import tensorflow as tf
DIR = "./MODEL"
from DataPipeline import *
#tf.enable_eager_execution()
print("TensorFlow version: {}".format(tf.VERSION))
#print("Eager execution: {}".format(tf.executing_eagerly()))
pipe = DataPipeline()
(train_feature, train_label), (test_feature, test_label) = pipe.load_data()

#Features ['ip','port','loc_country','zip','protocol','times']
loc_cul=tf.feature_column.categorical_column_with_vocabulary_list("loc_country", ["HU", "US", "PK", "RU", "MY", "SE", "KR"])
pro_cul=tf.feature_column.categorical_column_with_vocabulary_list("protocol", ["HTTP","HTTPS", "ICMP", "UDP","TCP"])
h_b_size = 100
e_c_size = h_b_size**0.25
ip_cul=tf.feature_column.categorical_column_with_hash_bucket("ip",h_b_size),


my_feature_columns = [
    tf.feature_column.embedding_column(categorical_column=ip_cul, dimension=e_c_size),
    tf.feature_column.numeric_column(key="port"),
    tf.feature_column.indicator_column(categorical_column=loc_cul),
    tf.feature_column.numeric_column(key="zip"),
    tf.feature_column.indicator_column(categorical_column=pro_cul),
    tf.feature_column.numeric_column(key="times")
]

classifier = tf.estimator.DNNClassifier(model_dir=DIR,feature_columns=my_feature_columns,hidden_units=[100, 50],n_classes=2)
print (train_feature)
print (test_label)
classifier.train(input_fn=lambda:pipe.train_input_fn(train_feature, train_label,batch_size=100) ,steps=10)


# Evaluate the model.

eval_result = classifier.evaluate(input_fn=lambda:pipe.eval_input_fn(test_feature, test_label, batch_size=40))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

#n_class tell possible number of value model can predict it could be attack or not attack meaning two outcomes
#he ideal batch size depends on the problem. As a rule of thumb, smaller batch sizes usually enable the train method to train the model faster at the expense (sometimes) of accuracy
#he default value of args.train_steps is 1000. The number of steps to train is a hyperparameter you can tune. Choosing the right number of steps usually requires both experience and experimentation.
