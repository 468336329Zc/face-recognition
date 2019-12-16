import facenet.src.align.detect_face
import facenet.src.facenet
import tensorflow as tf
from scipy import misc
import numpy as np


class faceAlign():
    def __init__(self):
        self.minsize = 20 # minimum size of face
        self.threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
        self.factor = 0.709 # scale factor
        self.gpu_memory_fraction = 1.0
        self.margin = 44
        self.image_size = 160

        with tf.Graph().as_default():
            self.gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=self.gpu_memory_fraction)
            self.sess = tf.Session(config=tf.ConfigProto(gpu_options=self.gpu_options, log_device_placement=False))
            with self.sess.as_default():
                self.pnet, self.rnet, self.onet = facenet.src.align.detect_face.create_mtcnn(self.sess, None)

    def align_start(self,arr_list):
        img_list = []
        rimg_list = []
        for image in arr_list:
            img = image
            img_size = np.asarray(img.shape)[0:2]
            bounding_boxes, _ = facenet.src.align.detect_face.detect_face(img, self.minsize, self.pnet, self.rnet, self.onet, self.threshold, self.factor)
            if len(bounding_boxes) < 1:
                arr_list.remove(image)
                continue
            for location in bounding_boxes:
                det = np.squeeze(location[0:4])
                bb = np.zeros(4, dtype=np.int32)
                bb[0] = np.maximum(det[0]-self.margin/2, 0)
                bb[1] = np.maximum(det[1]-self.margin/2, 0)
                bb[2] = np.minimum(det[2]+self.margin/2, img_size[1])
                bb[3] = np.minimum(det[3]+self.margin/2, img_size[0])
                cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
                aligned = misc.imresize(cropped, (self.image_size, self.image_size), interp='bilinear')
                prewhitened = facenet.src.facenet.prewhiten(aligned)
                img_list.append(prewhitened)
                rimg_list.append(cropped)
        try:
            images = np.stack(img_list)
            rimages = rimg_list
            return images,rimages
        except:
            return [],[]


