import torch
from dataset_loader import load_test_dataset  
from model import DigitCNN

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = DigitCNN().to(device)  
model.load_state_dict(torch.load('best_model.pth'))  

def test(model, test_loader, device):
    model.eval()  
    correct = 0
    total = 0

    with torch.no_grad():  
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)  # Move data to the appropriate device
            outputs = model(images)  # Get model predictions
            _, predicted = torch.max(outputs.data, 1)  # Get the index of the max log-probability
            total += labels.size(0)  # Total number of labels
            correct += (predicted == labels).sum().item()  # Count correct predictions

    accuracy = 100 * correct / total if total > 0 else 0  # Calculate accuracy
    print(f'Accuracy of the model on the test dataset: {accuracy:.2f}%')

test_loader = load_test_dataset(batch_size=32)  # Load the test dataset
test(model, test_loader, device)  # Call the test function
