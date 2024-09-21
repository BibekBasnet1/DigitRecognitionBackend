import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset_loader import load_dataset, load_test_dataset
from model import DigitCNN  
from utils import train, evaluate  

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_loader = load_dataset(batch_size=32)
val_loader = load_test_dataset(batch_size=32)  

model = DigitCNN().to(device)  
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

num_epochs = 30
best_val_loss = float('inf')  

for epoch in range(1, num_epochs + 1):
    print(f'Epoch {epoch}/{num_epochs}')

    train_loss = train(model, train_loader, optimizer, criterion, device)
    
    val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)  
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), 'best_model.pth')
        print("Model improved and saved.")

    scheduler.step()  

    print(f'Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.2f}')



# Validation Loader: Make sure you have a function to load the validation dataset (load_validation_dataset).
# Learning Rate Scheduler: A learning rate scheduler is set to reduce the learning rate every 10 epochs.
# Best Model Checkpointing: The model is saved when the validation loss improves.
# Print Messages: Added a message when the model improves and is saved for better tracking.
# Modular Imports: Ensure you have the necessary imports for evaluate from utils.
