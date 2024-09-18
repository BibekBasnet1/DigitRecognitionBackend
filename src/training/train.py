import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset_loader import load_dataset  
from model import DigitCNN  
from utils import train, validate  

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load dataset
train_loader, val_loader = load_dataset(batch_size=32)

# Initialize model, optimizer, and loss function
model = DigitCNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training parameters
num_epochs = 10

for epoch in range(1, num_epochs + 1):
    print(f'Epoch {epoch}/{num_epochs}')
    
    # Train and validate the model
    train(model, train_loader, optimizer, criterion, device)
    validate(model, val_loader, criterion, device)

# Save the trained model
torch.save(model.state_dict(), 'digit_cnn.pth')
