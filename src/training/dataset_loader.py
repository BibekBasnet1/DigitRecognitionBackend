import os
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

def load_dataset(batch_size=32, train_split=0.8):
    transform = transforms.Compose([
        transforms.Grayscale(),  # Convert to grayscale
        transforms.Resize((28, 28)),  # Resize to 28x28
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize((0.5,), (0.5,))  # Normalize to [-1, 1]
    ])

    # Dynamically locate the dataset directory
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    dataset_dir = os.path.join(base_dir, '..', 'dataset')  # Navigate to the dataset folder

    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")
    
    # Load the dataset from the folder
    dataset = datasets.ImageFolder(root=dataset_dir, transform=transform)

    # Split dataset into training and validation sets
    train_size = int(train_split * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader
