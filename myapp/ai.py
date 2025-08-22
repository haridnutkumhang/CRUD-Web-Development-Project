import torch
import torch.nn as nn
import torch.nn.functional as F

class GrayscaleImageNet (nn.Module):
    def __init__(self):
        super(GrayscaleImageNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, 7, 2, 3)
        self.pool1 = nn.MaxPool2d(3, 3)
        self.conv2 = nn.Conv2d(10, 20, 5, 1, 2)
        self.pool2 = nn.AvgPool2d(2, 2)
        self.fc1 = nn.Linear(20 * 5 * 5, 150)
        self.fc2 = nn.Linear(150, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        x = torch.flatten(x,1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        x = F.softmax(x, dim=1)
        return x
    
if __name__ == '__main__':
    model = GrayscaleImageNet()
    dummy_input = torch.randn(8,1,64,64)
    output = model(dummy_input)
    print("Output shape:" , output.shape)