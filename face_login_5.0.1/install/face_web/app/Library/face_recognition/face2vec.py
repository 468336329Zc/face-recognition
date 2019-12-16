import facenet.src.facenet
import tensorflow as tf
import os

class face2vec():
    def __init__(self):
        self.modeldir = "20180408-102900"
        self.model = os.path.normpath(os.path.join(
                            os.getcwd(), 
                            os.path.dirname(__file__), 
                            'train_model/%s'%(self.modeldir)))
        self.sess = tf.Session()
        self.meta_file, self.ckpt_file = facenet.src.facenet.get_model_filenames(self.model)

        #print('Metagraph file: %s' % self.meta_file)
        #print('Checkpoint file: %s' % self.ckpt_file)
        print("Using model:%s"%(self.modeldir))
        self.load_model(self.sess,self.model, self.meta_file, self.ckpt_file)

        # Get input and output tensors
        self.images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")

        self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")

        self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

        self.image_size = self.images_placeholder.get_shape()[1]
        #print("image_size:",self.image_size)

        self.embedding_size = self.embeddings.get_shape()[1]

        # Run forward pass to calculate embeddings
        #print('Runnning forward pass on images') 


    def compute_facial_encodings(self,nrof_images,nrof_batches,emb_array,batch_size,paths,pathsid):
        for i in range(nrof_batches):
            start_index = i*batch_size
            end_index = min((i+1)*batch_size, nrof_images)
            paths_batch = paths[start_index:end_index]
            images = paths_batch
            feed_dict = { self.images_placeholder:images, self.phase_train_placeholder:False }
            emb_array[start_index:end_index,:] = self.sess.run(self.embeddings, feed_dict=feed_dict)

        facial_encodings = {}
        for x in range(nrof_images):
            facial_encodings[pathsid[x]] = emb_array[x,:]

        return facial_encodings


    def load_model(self,sess,model_dir, meta_file, ckpt_file):
        model_dir_exp = os.path.expanduser(model_dir)
        saver = tf.train.import_meta_graph(os.path.join(model_dir_exp, meta_file))
        saver.restore(sess, os.path.join(model_dir_exp, ckpt_file))
