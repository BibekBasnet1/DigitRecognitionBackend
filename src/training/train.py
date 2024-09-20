import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset_loader import load_dataset, load_test_dataset  
from model import DigitCNN  
from utils import train  

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the training dataset
train_loader = load_dataset(batch_size=32)

model = DigitCNN().to(device)  # Move the model to the specified device
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

num_epochs = 30

for epoch in range(1, num_epochs + 1):
    print(f'Epoch {epoch}/{num_epochs}')
    
    train(model, train_loader, optimizer, criterion, device)

torch.save(model.state_dict(), 'fourth_model.pth')

# test_loader = load_test_dataset(batch_size=32)
