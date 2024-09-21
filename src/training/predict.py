import torch
from fastapi import HTTPException
from PIL import Image
from torchvision import transforms
from src.training.load_model import load_trained_model


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = load_trained_model().to(device)  

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((28, 28)),  
        transforms.ToTensor(),  
        transforms.Normalize((0.5,), (0.5,))  
    ])
    
    try:
        image = Image.open(image_path).convert("L")  

        # Binarization: Thresholding to create a binary image
        image = image.point(lambda p: 255 if p > 128 else 0)  # Invert if necessary

        # Apply the transformations
        image = transform(image)
        image = image.unsqueeze(0)  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")
    
    return image

def predict(image_path):
    image = preprocess_image(image_path)
    image = image.to(device)  

    try:
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
    return predicted.item() 
