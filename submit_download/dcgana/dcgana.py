""" Deep Convolutional Generative Adversarial Network (DCGAN).

Using deep convolutional generative adversarial networks (DCGAN) to generate
digit images from a noise distribution.

References:
    - Unsupervised representation learning with deep convolutional generative
    adversarial networks. A Radford, L Metz, S Chintala. arXiv:1511.06434.

Links:
    - [DCGAN Paper](https://arxiv.org/abs/1511.06434).
    - [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import division, print_function, absolute_import

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import csv
import numpy as np
import psutil
import os
import cpuinfo
import datetime
import time
import numpy
# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data

process = psutil.Process(os.getpid())
no_core = psutil.cpu_count(logical=True)
processor = cpuinfo.get_cpu_info()['brand_raw']
time.sleep(5)

initial_usage = psutil.cpu_percent()
core = []
for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
    print ("core("+str(i)+")"+str(percentage)+"%")
    core.append(percentage)
total_mem = float(psutil.virtual_memory().total/(1024.0**3.0))
avail_mem = float(psutil.virtual_memory().available/(1024.0**3.0))
avail_mem_per = (float(psutil.virtual_memory().available/(1024.0**3.0))*100)/(float(psutil.virtual_memory().total/(1024.0**3.0)))
used_mem = float(psutil.virtual_memory().total/(1024.0**3.0))-float(psutil.virtual_memory().available/(1024.0**3.0))
used_mem_per = ((float(psutil.virtual_memory().total/(1024.0**3.0))-float(psutil.virtual_memory().available/(1024.0**3.0)))*100)/(float(psutil.virtual_memory().total/(1024.0**3.0)))

start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
ff_name="/opt/"+str(datetime.datetime.now().day)+"_"+str(datetime.datetime.now().month)+"_"+str(datetime.datetime.now().year)+"_"+str(datetime.datetime.now().hour)+"_"+str(datetime.datetime.now().minute)+"_"+str(datetime.datetime.now().second)+".csv"
#batch_size = 128
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)
info_file_name = "/opt/degan.csv"
# Training Params
num_steps = 20000
batch_size = 32

# Network Params
image_dim = 784 # 28*28 pixels * 1 channel
gen_hidden_dim = 256
disc_hidden_dim = 256
noise_dim = 200 # Noise data points


# Generator Network
# Input: Noise, Output: Image
def generator(x, reuse=False):
    with tf.variable_scope('Generator', reuse=reuse):
        # TensorFlow Layers automatically create variables and calculate their
        # shape, based on the input.
        x = tf.layers.dense(x, units=6 * 6 * 128)
        x = tf.nn.tanh(x)
        # Reshape to a 4-D array of images: (batch, height, width, channels)
        # New shape: (batch, 6, 6, 128)
        x = tf.reshape(x, shape=[-1, 6, 6, 128])
        # Deconvolution, image shape: (batch, 14, 14, 64)
        x = tf.layers.conv2d_transpose(x, 64, 4, strides=2)
        # Deconvolution, image shape: (batch, 28, 28, 1)
        x = tf.layers.conv2d_transpose(x, 1, 2, strides=2)
        # Apply sigmoid to clip values between 0 and 1
        x = tf.nn.sigmoid(x)
        return x
def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)

def combine_file(ff_name, start_time, start_date, finish_time, finish_date, finish_total, start_total, total_mem, avail_mem, avail_mem_per, used_mem, used_mem_per,mem,processor,initial_usage,final_usage,no_core,tp12):
    with open(ff_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Start/Finish/Executing Time"])
        csvwriter.writerow(["Starting time(h:m:s)-"+start_time+" ("+start_date+")"])
        csvwriter.writerow(["Finishing time(h:m:s)-"+finish_time+" ("+finish_date+")"])
        csvwriter.writerow(["Total execution time :"+ convert(finish_total-start_total)])
        csvwriter.writerow([""])
        csvwriter.writerow([""])
        csvwriter.writerow(["Memory Information"])
        csvwriter.writerow([""])
        csvwriter.writerow(["Total Memory:"+str(total_mem)+"GB(100%)"])
        csvwriter.writerow(["Available memory:"+ str(avail_mem)+" GB("+str(avail_mem_per)+"%)"])
        csvwriter.writerow(["Used memory:"+ str(used_mem)+" GB("+str(used_mem_per)+"%)"])
        csvwriter.writerow(["Occupied memory for this job:"+str(mem)+"%"])
        csvwriter.writerow([""])
        csvwriter.writerow([""])
        csvwriter.writerow(["CPU Information"])
        csvwriter.writerow(["Processor:"+ processor])
        csvwriter.writerow(["Initial CPU load:"+str(initial_usage)+"%"])
        csvwriter.writerow(["Final CPU Usage :"+ str(final_usage)+"%"])
        csvwriter.writerow(["Occupied CPU for this job:"+str(final_usage-initial_usage)+"%"])
        csvwriter.writerow(["Total cores:", str(no_core)])
        csvwriter.writerows(tp12)
        csvwriter.writerow([""])
        csvwriter.writerow([""])
        csvwriter.writerow(["Program Results"])
        #csvwriter.writerow(["Test score:"+str(sco)])
        #csvwriter.writerow(["Test accuracy:"+str(acc)])
#def final_read_combine(info_file_name, i, gl, dl):
#    with open(info_file_name, 'a')as csvfile:
#        csvwriter = csv.writer(csvfile)
#        csvwriter.writerow(['Step %i: Generator Loss: %f, Discriminator Loss: %f' % (i, gl, dl)])
# Discriminator Network
# Input: Image, Output: Prediction Real/Fake Image
def discriminator(x, reuse=False):
    with tf.variable_scope('Discriminator', reuse=reuse):
        # Typical convolutional neural network to classify images.
        x = tf.layers.conv2d(x, 64, 5)
        x = tf.nn.tanh(x)
        x = tf.layers.average_pooling2d(x, 2, 2)
        x = tf.layers.conv2d(x, 128, 5)
        x = tf.nn.tanh(x)
        x = tf.layers.average_pooling2d(x, 2, 2)
        x = tf.contrib.layers.flatten(x)
        x = tf.layers.dense(x, 1024)
        x = tf.nn.tanh(x)
        # Output 2 classes: Real and Fake images
        x = tf.layers.dense(x, 2)
    return x

# Build Networks
# Network Inputs
noise_input = tf.placeholder(tf.float32, shape=[None, noise_dim])
real_image_input = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])

# Build Generator Network
gen_sample = generator(noise_input)

# Build 2 Discriminator Networks (one from real image input, one from generated samples)
disc_real = discriminator(real_image_input)
disc_fake = discriminator(gen_sample, reuse=True)
disc_concat = tf.concat([disc_real, disc_fake], axis=0)

# Build the stacked generator/discriminator
stacked_gan = discriminator(gen_sample, reuse=True)

# Build Targets (real or fake images)
disc_target = tf.placeholder(tf.int32, shape=[None])
gen_target = tf.placeholder(tf.int32, shape=[None])

# Build Loss
disc_loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
    logits=disc_concat, labels=disc_target))
gen_loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
    logits=stacked_gan, labels=gen_target))

# Build Optimizers
optimizer_gen = tf.train.AdamOptimizer(learning_rate=0.001)
optimizer_disc = tf.train.AdamOptimizer(learning_rate=0.001)

# Training Variables for each optimizer
# By default in TensorFlow, all variables are updated by each optimizer, so we
# need to precise for each one of them the specific variables to update.
# Generator Network Variables
gen_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Generator')
# Discriminator Network Variables
disc_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='Discriminator')

# Create training operations
train_gen = optimizer_gen.minimize(gen_loss, var_list=gen_vars)
train_disc = optimizer_disc.minimize(disc_loss, var_list=disc_vars)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training
with tf.Session() as sess:

    # Run the initializer
    sess.run(init)

    for i in range(1, num_steps+1):

        # Prepare Input Data
        # Get the next batch of MNIST data (only images are needed, not labels)
        batch_x, _ = mnist.train.next_batch(batch_size)
        batch_x = np.reshape(batch_x, newshape=[-1, 28, 28, 1])
        # Generate noise to feed to the generator
        z = np.random.uniform(-1., 1., size=[batch_size, noise_dim])

        # Prepare Targets (Real image: 1, Fake image: 0)
        # The first half of data fed to the discriminator are real images,
        # the other half are fake images (coming from the generator).
        batch_disc_y = np.concatenate(
            [np.ones([batch_size]), np.zeros([batch_size])], axis=0)
        # Generator tries to fool the discriminator, thus targets are 1.
        batch_gen_y = np.ones([batch_size])

        # Training
        feed_dict = {real_image_input: batch_x, noise_input: z,
                     disc_target: batch_disc_y, gen_target: batch_gen_y}
        _, _, gl, dl = sess.run([train_gen, train_disc, gen_loss, disc_loss],
                                feed_dict=feed_dict)
        if i % 100 == 0 or i == 1:
            #print('Step %i: Generator Loss: %f, Discriminator Loss: %f' % (i, gl, dl))
            if (i<7000):
                print('Step %i: Generator Loss: %f, Discriminator Loss: %f' % (i, gl, dl))
                with open(info_file_name, 'a')as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(['Step %i: Generator Loss: %f, Discriminator Loss: %f' % (i, gl, dl)])
                    continue
            else:
                print ("Over 7000")
                print('Step %i: Generator Loss: %f, Discriminator Loss: %f' % (i, gl, dl))
                continue
            #final_read_combine(info_file_name, i, gl, dl)

    # Generate images from noise, using the generator network.
    f, a = plt.subplots(4, 10, figsize=(10, 4))
    for i in range(10):
        # Noise input.
        z = np.random.uniform(-1., 1., size=[4, noise_dim])
        g = sess.run(gen_sample, feed_dict={noise_input: z})
        for j in range(4):
            # Generate image from noise. Extend to 3 channels for matplot figure.
            img = np.reshape(np.repeat(g[j][:, :, np.newaxis], 3, axis=2),
                             newshape=(28, 28, 3))
            #a[j][i].imshow(img)

    #f.show()
    plt.draw()
    #plt.waitforbuttonpress()
    #plt.savefig('/opt/waitforbuttonpress')

mem = process.memory_percent()
final_usage = psutil.cpu_percent()
finish_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
finish_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
finish_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
print ("="*10, "Start/Finish/Execution Time", "="*10)
print ("Starting time(h:m:s)-"+start_time+" ("+start_date+")")
print ("Finishing time(h:m:s)-"+finish_time+" ("+finish_date+")")
print ("Total execution time :"+ convert(finish_total-start_total))

print ("="*10, "Memory Information", "="*10)
print ("Total memory:"+ str(total_mem)+"GB(100%)")
print ("Available memory:"+ str(avail_mem)+" GB("+str(avail_mem_per)+"%)")
print ("Used memory:"+ str(used_mem)+" GB("+str(used_mem_per)+"%)")
print ("Occupied memory for this job:"+str(mem)+"%")
core_name = []
core_usg = []
    
print ("="*10, "CPU Information", "="*10)
print ("Processor:"+ processor)
print ("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
    print ("core("+str(i)+")"+str(percentage)+"%")
    core_name.append("core("+str(i)+")")
    core_usg.append(str(percentage)+"%")
tp1 = numpy.array(core_name)
tp2 = numpy.array(core_usg)
tp12 = numpy.vstack((tp1, tp2)).T
print ("Initial CPU load:"+str(initial_usage)+"%")
print ("Final CPU Usage :"+ str(final_usage)+"%")
print ("Occupied CPU for this job:"+str(final_usage-initial_usage)+"%")
combine_file(ff_name,start_time, start_date, finish_time, finish_date, finish_total, start_total,total_mem,avail_mem,avail_mem_per,used_mem,used_mem_per,mem,processor,initial_usage,final_usage,no_core,tp12)
    #time.sleep(3600)