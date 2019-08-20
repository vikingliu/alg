import tensorflow as tf


#
# SqueezeNet是Han等提出的一种轻量且高效的CNN模型，它参数比AlexNet少50x，但模型性能（accuracy）与AlexNet接近。
#
# 在可接受的性能下，小模型相比大模型，具有很多优势：
#
# 1.更高效的分布式训练，小模型参数小，网络通信量减少；
#
# 2.便于模型更新，模型小，客户端程序容易更新；
#
# 3.利于部署在特定硬件如FPGA，因为其内存受限。因此研究小模型是很有现实意义的。
#
#
#
# Han等将CNN模型设计的研究总结为四个方面：
#
# 1.模型压缩：对pre-trained的模型进行压缩，使其变成小模型，如采用网络剪枝和量化等手段；
#
# 2.对单个卷积层进行优化设计，如采用1x1的小卷积核，还有很多采用可分解卷积（factorized convolution）结构或者模块化的结构（blocks, modules）；
#
# 3.网络架构层面上的优化设计，如网路深度（层数），还有像ResNet那样采用“短路”连接（bypass connection）；
#
# 4.不同超参数、网络结构，优化器等的组合优化。
#
#
#
# SqueezeNet也是从这四个方面来进行设计的，其设计理念可以总结为以下三点：
#
# 1.大量使用1x1卷积核替换3x3卷积核，因为参数可以降低9倍；
#
# 2.减少3x3卷积核的输入通道数（input channels），因为卷积核参数为：(number of input channels) * (number of filters) * 3 * 3.
#
# 3.延迟下采样（downsample），前面的layers可以有更大的特征图，有利于提升模型准确度。目前下采样一般采用strides>1的卷积层或者pool layer。
class SqueezeNet(object):
    def __init__(self, inputs, nb_classes=1000, is_training=True):
        # conv1
        net = tf.layers.conv2d(inputs, 96, [7, 7], strides=[2, 2],
                               padding="SAME", activation=tf.nn.relu,
                               name="conv1")
        # maxpool1
        net = tf.layers.max_pooling2d(net, [3, 3], strides=[2, 2],
                                      name="maxpool1")
        # fire2
        net = self._fire(net, 16, 64, "fire2")
        # fire3
        net = self._fire(net, 16, 64, "fire3")
        # fire4
        net = self._fire(net, 32, 128, "fire4")
        # maxpool4
        net = tf.layers.max_pooling2d(net, [3, 3], strides=[2, 2],
                                      name="maxpool4")
        # fire5
        net = self._fire(net, 32, 128, "fire5")
        # fire6
        net = self._fire(net, 48, 192, "fire6")
        # fire7
        net = self._fire(net, 48, 192, "fire7")
        # fire8
        net = self._fire(net, 64, 256, "fire8")
        # maxpool8
        net = tf.layers.max_pooling2d(net, [3, 3], strides=[2, 2],
                                      name="maxpool8")
        # fire9
        net = self._fire(net, 64, 256, "fire9")
        # dropout
        net = tf.layers.dropout(net, 0.5, training=is_training)
        # conv10
        net = tf.layers.conv2d(net, 1000, [1, 1], strides=[1, 1],
                               padding="SAME", activation=tf.nn.relu,
                               name="conv10")
        # avgpool10
        net = tf.layers.average_pooling2d(net, [13, 13], strides=[1, 1],
                                          name="avgpool10")
        # squeeze the axis
        net = tf.squeeze(net, axis=[1, 2])

        self.logits = net
        self.prediction = tf.nn.softmax(net)

    def _fire(self, inputs, squeeze_depth, expand_depth, scope):
        with tf.variable_scope(scope):
            # squeeze
            squeeze = tf.layers.conv2d(inputs, squeeze_depth, [1, 1],
                                       strides=[1, 1], padding="SAME",
                                       activation=tf.nn.relu, name="squeeze")

            expand_1x1 = tf.layers.conv2d(squeeze, expand_depth, [1, 1],
                                          strides=[1, 1], padding="SAME",
                                          activation=tf.nn.relu, name="expand_1x1")
            expand_3x3 = tf.layers.conv2d(squeeze, expand_depth, [3, 3],
                                          strides=[1, 1], padding="SAME",
                                          activation=tf.nn.relu, name="expand_3x3")
            return tf.concat([expand_1x1, expand_3x3], axis=3)
