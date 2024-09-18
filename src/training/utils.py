import torch

def train(model, train_loader, optimizer, criterion, device):
    model.train()
    running_loss = 0.0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        output = model(data)

        # Compute loss and backpropagate
        loss = criterion(output, target)
        loss.backward()

        # Optimize the weights
        optimizer.step()

        running_loss += loss.item()

        if batch_idx % 10 == 0:
            print(f'Train Batch {batch_idx}: Loss = {loss.item()}')

    return running_loss / len(train_loader)

def validate(model, val_loader, criterion, device):
    model.eval()
    val_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in val_loader:
            data, target = data.to(device), target.to(device)
            
            # Forward pass
            output = model(data)
            val_loss += criterion(output, target).item()
            
            # Get the index of the max log-probability (predicted digit)
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    val_loss /= len(val_loader.dataset)
    accuracy = 100. * correct / len(val_loader.dataset)
    
    print(f'Validation Loss: {val_loss:.4f}, Accuracy: {accuracy:.2f}%')
    
    return val_loss, accuracy
