from __future__ import print_function
import numpy as np
import pandas as pd
import tensorflow as tf
import math as math
import argparse
class DataPipeline:
  '''
  def train_input_fn(self,features, labels, batch_size):
      """An input function for training"""
      # Convert the inputs to a Dataset.
      dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

      # Shuffle, repeat, and batch the examples.
      dataset = dataset.shuffle(1000).repeat().batch(batch_size)

      # Return the dataset.
      return dataset
  '''
  #Google Train input function
  def eval_input_fn(self,features, labels=None, batch_size=None):
    if labels is None:
        dataset = tf.data.Dataset.from_tensor_slices(dict(features))
    else:
        dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)
    # Return the read end of the pipeline.
    return dataset.make_one_shot_iterator().get_next()


  def train_input_fn(self,features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    # Setting the buffer_size to a value larger than the number of examples (120) buffer size 1000 ensures that the data will be well shuffled.
    #examples 1000 buffere size 10000
    dataset = dataset.shuffle(buffer_size=100000).repeat(count=5).batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()

  TRAIN_URL = "./train_test_data/data_train.csv"
  TEST_URL = "./train_test_data/data_test.csv"

  CSV_COLUMN_NAMES = ['ip','port','loc_country','zip','protocol','ts','times','is_attack']


  def load_data(self,label_name='is_attack'):
      """Parses the csv file in TRAIN_URL and TEST_URL."""

      # Parse the local CSV file.
      train = pd.read_csv(filepath_or_buffer=self.TRAIN_URL,
                          names=self.CSV_COLUMN_NAMES,  # list of column names
                          dtype={"ip": str,"loc_country":str,"protocol":str},
                          header=0  # ignore the first row of the CSV file.
                         )
      # train now holds a pandas DataFrame, which is data structure
      # analogous to a table.

      # 1. Assign the DataFrame's labels (the right-most column) to train_label.
      # 2. Delete (pop) the labels from the DataFrame.
      # 3. Assign the remainder of the DataFrame to train_features

      # poping ts because it's of no use maybe in future models
      train.pop('ts')


      train_features, train_label = train, train.pop(label_name)



      # Apply the preceding logic to the test set.
      test = pd.read_csv(self.TEST_URL, names=self.CSV_COLUMN_NAMES, header=0)
      test.pop('ts')
      test_features, test_label = test, test.pop(label_name)

      # Return four DataFrames.
      return (train_features, train_label), (test_features, test_label)