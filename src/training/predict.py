import torch
from fastapi import HTTPException
from PIL import Image
from torchvision import transforms
from src.training.load_model import load_trained_model

model = load_trained_model()

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    try:
        image = Image.open(image_path)
        image = transform(image)
        image = image.unsqueeze(0)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")
    
    return image

def predict(image_path):
    image = preprocess_image(image_path)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    image = image.to(device)

    try:
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
    return predicted.item()
