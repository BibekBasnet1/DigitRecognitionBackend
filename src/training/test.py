import torch
from dataset_loader import load_test_dataset  
from model import DigitCNN
import numpy as np
from sklearn.metrics import confusion_matrix

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


model = DigitCNN().to(device)  
model.load_state_dict(torch.load('third_model.pth'))  

# def test(model, test_loader, device):
#     model.eval()  
#     correct = 0
#     total = 0

#     with torch.no_grad():  
#         for images, labels in test_loader:
#             images, labels = images.to(device), labels.to(device)  # Move data to the appropriate device
#             outputs = model(images)  # Get model predictions
#             _, predicted = torch.max(outputs.data, 1)  # Get the index of the max log-probability
#             total += labels.size(0)  # Total number of labels
#             correct += (predicted == labels).sum().item()  # Count correct predictions

#     accuracy = 100 * correct / total if total > 0 else 0  # Calculate accuracy
#     print(f'Accuracy of the model on the test dataset: {accuracy:.2f}%')

# test_loader = load_test_dataset(batch_size=32)  
# test(model, test_loader, device)  

def test_with_confusion_matrix(model, test_loader, device):
    model.eval()
    all_labels = []
    all_predictions = []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            
            # Store all labels and predictions for confusion matrix
            all_labels.extend(labels.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())

    # Calculate confusion matrix
    conf_matrix = confusion_matrix(all_labels, all_predictions)
    print("Confusion Matrix:\n", conf_matrix)

    # Calculate accuracy
    accuracy = 100 * np.trace(conf_matrix) / np.sum(conf_matrix)
    print(f'Accuracy of the model on the test dataset: {accuracy:.2f}%')

test_loader = load_test_dataset(batch_size=32)
test_with_confusion_matrix(model, test_loader, device)
