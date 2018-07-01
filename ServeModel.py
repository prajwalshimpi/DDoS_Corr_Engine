import tensorflow as tf
session = tf.Session()
saver = tf.train.import_meta_graph( './MODEL/model.ckpt-15000.meta')
saver.restore(session, '.mp/model.ckpt-15000.data-00')
