import torch.nn as nn
import torch
import torch.optim as optim
import numpy as np


class Generator(nn.Module):
    def __init__(self, inputc, outputc):
        '''
        Generator is Encoder-Decoder structure

        inputc: number of input channel
        outputc: number of output channel
        '''
        super(Generator, self).__init__()
        self.conv1 = nn.Conv2d(inputc, 64, kernel_size=4, padding=1, stride=2)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=4, padding=1, stride=2)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=4, padding=1, stride=2)
        self.bn3 = nn.BatchNorm2d(256)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=4, padding=1, stride=2)
        self.bn4 = nn.BatchNorm2d(512)
        self.conv5 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn5 = nn.BatchNorm2d(512)
        self.conv6 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn6 = nn.BatchNorm2d(512)
        self.conv7 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn7 = nn.BatchNorm2d(512)
        self.conv8 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn8 = nn.BatchNorm2d(512)
        self.relu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

        self.deconv1 = nn.ConvTranspose2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn1_d = nn.BatchNorm2d(512)
        self.deconv2 = nn.ConvTranspose2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn2_d = nn.BatchNorm2d(512)
        self.deconv3 = nn.ConvTranspose2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn3_d = nn.BatchNorm2d(512)
        self.deconv4 = nn.ConvTranspose2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn4_d = nn.BatchNorm2d(512)
        self.deconv5 = nn.ConvTranspose2d(512, 256, kernel_size=4, padding=1, stride=2)
        self.bn5_d = nn.BatchNorm2d(256)
        self.deconv6 = nn.ConvTranspose2d(256, 128, kernel_size=4, padding=1, stride=2)
        self.bn6_d = nn.BatchNorm2d(128)
        self.deconv7 = nn.ConvTranspose2d(128, 64, kernel_size=4, padding=1, stride=2)
        self.bn7_d = nn.BatchNorm2d(64)
        self.deconv8 = nn.ConvTranspose2d(64, outputc, kernel_size=4, padding=1, stride=2)
        self.bn8_d = nn.BatchNorm2d(outputc)
        self.dropout = nn.Dropout(p=0.5)
        self.tanh = nn.Tanh()

    def forward(self, x):
        '''
        x: expected shape N*C*256*256
        '''
        # encoder
        x = self.conv1(x)  # shape: N * 64 * 128 * 128
        # x = self.relu(self.bn1(self.conv1(x)))  # shape: N * 64 * 128 * 128
        x = self.relu(self.bn2(self.conv2(x)))  # shape: N * 128 * 64 * 64
        x = self.relu(self.bn3(self.conv3(x)))  # shape: N * 256 * 32 * 32
        x = self.relu(self.bn4(self.conv4(x)))  # shape: N * 512 * 16 * 16
        x = self.relu(self.bn5(self.conv5(x)))  # shape: N * 512 * 8 * 8
        x = self.relu(self.bn6(self.conv6(x)))  # shape: N * 512 * 4 * 4
        x = self.relu(self.bn7(self.conv7(x)))  # shape: N * 512 * 2 * 2
        x = self.relu(self.bn8(self.conv8(x)))  # shape: N * 512 * 1 * 1

        # decoder
        x = self.relu(self.dropout(self.bn1_d(self.deconv1(x))))    # shape: N * 512 * 2 * 2
        x = self.relu(self.dropout(self.bn2_d(self.deconv2(x))))    # shape: N * 512 * 4 * 4
        x = self.relu(self.dropout(self.bn3_d(self.deconv3(x))))    # shape: N * 512 * 8 * 8
        x = self.relu(self.bn4_d(self.deconv4(x)))    # shape: N * 512 * 16 * 16
        x = self.relu(self.bn5_d(self.deconv5(x)))   # shape: N * 256 * 32 * 32
        x = self.relu(self.bn6_d(self.deconv6(x)))    # shape: N * 128 * 64 * 64
        x = self.relu(self.bn7_d(self.deconv7(x)))   # shape: N * 64 * 128 * 128 
        x = self.relu(self.bn8_d(self.deconv8(x)))    # shape: N * outputC * 256 * 256
        x = self.tanh(x)
        return x


class UNetGenerator(nn.Module):
    def __init__(self, inputc, outputc):
        super(UNetGenerator, self).__init__()
        self.conv1 = nn.Conv2d(inputc, 64, kernel_size=4, padding=1, stride=2)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=4, padding=1, stride=2)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=4, padding=1, stride=2)
        self.bn3 = nn.BatchNorm2d(256)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=4, padding=1, stride=2)
        self.bn4 = nn.BatchNorm2d(512)
        self.conv5 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn5 = nn.BatchNorm2d(512)
        self.conv6 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn6 = nn.BatchNorm2d(512)
        self.conv7 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn7 = nn.BatchNorm2d(512)
        self.conv8 = nn.Conv2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn8 = nn.BatchNorm2d(512)
        self.relu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

        self.deconv1 = nn.ConvTranspose2d(512, 512, kernel_size=4, padding=1, stride=2)
        self.bn1_d = nn.BatchNorm2d(512)
        self.deconv2 = nn.ConvTranspose2d(1024, 512, kernel_size=4, padding=1, stride=2)
        self.bn2_d = nn.BatchNorm2d(512)
        self.deconv3 = nn.ConvTranspose2d(1024, 512, kernel_size=4, padding=1, stride=2)
        self.bn3_d = nn.BatchNorm2d(512)
        self.deconv4 = nn.ConvTranspose2d(1024, 512, kernel_size=4, padding=1, stride=2)
        self.bn4_d = nn.BatchNorm2d(512)
        self.deconv5 = nn.ConvTranspose2d(1024, 256, kernel_size=4, padding=1, stride=2)
        self.bn5_d = nn.BatchNorm2d(256)
        self.deconv6 = nn.ConvTranspose2d(512, 128, kernel_size=4, padding=1, stride=2)
        self.bn6_d = nn.BatchNorm2d(128)
        self.deconv7 = nn.ConvTranspose2d(256, 64, kernel_size=4, padding=1, stride=2)
        self.bn7_d = nn.BatchNorm2d(64)
        self.deconv8 = nn.ConvTranspose2d(128, outputc, kernel_size=4, padding=1, stride=2)
        self.bn8_d = nn.BatchNorm2d(outputc)
        self.dropout = nn.Dropout(p=0.5)
        self.tanh = nn.Tanh()

    def forward(self, x):
        '''
        x: expected shape N*C*256*256
        '''
        # encoder
        x1 = self.relu(self.conv1(x))  # shape: N * 64 * 128 * 128
        # x = self.relu(self.bn1(self.conv1(x)))  # shape: N * 64 * 128 * 128
        x2 = self.relu(self.bn2(self.conv2(x1)))  # shape: N * 128 * 64 * 64
        x3 = self.relu(self.bn3(self.conv3(x2)))  # shape: N * 256 * 32 * 32
        x4 = self.relu(self.bn4(self.conv4(x3)))  # shape: N * 512 * 16 * 16
        x5 = self.relu(self.bn5(self.conv5(x4)))  # shape: N * 512 * 8 * 8
        x6 = self.relu(self.bn6(self.conv6(x5)))  # shape: N * 512 * 4 * 4
        x7 = self.relu(self.bn7(self.conv7(x6)))  # shape: N * 512 * 2 * 2
        x8 = self.relu(self.bn8(self.conv8(x7)))  # shape: N * 512 * 1 * 1

        # decoder
        x_1 = self.relu(self.dropout(self.bn1_d(self.deconv1(x8))))    # shape: N * 512 * 2 * 2
        x_1 = torch.cat((x_1, x7), 1)                                   # shape: N * 1024 * 2 * 2
        x_2 = self.relu(self.dropout(self.bn2_d(self.deconv2(x_1))))    # shape: N * 512 * 4 * 4
        x_2 = torch.cat((x_2, x6), 1)                                   # shape: N * 1024 * 4 * 4
        x_3 = self.relu(self.dropout(self.bn3_d(self.deconv3(x_2))))    # shape: N * 512 * 8 * 8
        x_3 = torch.cat((x_3, x5), 1)                                   # shape: N * 1024 * 8 * 8
        x_4 = self.relu(self.bn4_d(self.deconv4(x_3)))                  # shape: N * 512 * 16 * 16
        x_4 = torch.cat((x_4, x4), 1)                                   # shape: N * 1024 * 16 * 16
        x_5 = self.relu(self.bn5_d(self.deconv5(x_4)))                  # shape: N * 256 * 32 * 32
        x_5 = torch.cat((x_5, x3), 1)                                   # shape: N * 512 * 32 * 32
        x_6 = self.relu(self.bn6_d(self.deconv6(x_5)))                  # shape: N * 128 * 64 * 64
        x_6 = torch.cat((x_6, x2), 1)                                   # shape: N * 256 * 64 * 64
        x_7 = self.relu(self.bn7_d(self.deconv7(x_6)))                  # shape: N * 64 * 128 * 128 
        x_7 = torch.cat((x_7, x1), 1)                                   # shape: N * 128 * 128 * 128
        x_8 = self.relu(self.deconv8(x_7))                              # shape: N * outputC * 256 * 256
        x = self.tanh(x)
        return x




