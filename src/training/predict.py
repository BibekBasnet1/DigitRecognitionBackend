import torch
from fastapi import HTTPException
from PIL import Image
from torchvision import transforms
from src.training.load_model import load_trained_model

# Load and prepare the model once
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = load_trained_model().to(device)  # Move model to the correct device

# def preprocess_image(image_path):
#     transform = transforms.Compose([
#         transforms.Grayscale(),  # Ensure image is grayscale
#         transforms.Resize((28, 28)),  # Resize to 28x28
#         transforms.ToTensor(),  # Convert to tensor
#         transforms.Normalize((0.5,), (0.5,))  # Normalize
#     ])

#     try:
#         image = Image.open(image_path).convert("RGB")  # Ensure image is in RGB format
#         image = transform(image)
#         image = image.unsqueeze(0)  # Add batch dimension
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")
    
#     return image

# def predict(image_path):
#     image = preprocess_image(image_path)
#     image = image.to(device)  # Move image to the same device as model

#     try:
#         with torch.no_grad():
#             output = model(image)
#             _, predicted = torch.max(output, 1)  # Get the predicted class
#     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
# #     return predicted.item()  # Return the predicted class index
# def preprocess_image(image_path):
#     transform = transforms.Compose([
#         transforms.Grayscale(),  # Ensure image is grayscale
#         transforms.Resize((28, 28)),  # Resize to 28x28
#         transforms.ToTensor(),  # Convert to tensor
#         transforms.Normalize((0.5,), (0.5,))  # Normalize
#     ])

#     try:
#         image = Image.open(image_path).convert("L")  # Convert to grayscale
#         image = transform(image)
#         image = image.unsqueeze(0)  # Add batch dimension
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")
    
#     return image

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Grayscale(),  # Convert to grayscale
        transforms.Resize((28, 28)),  # Resize to 28x28
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize((0.5,), (0.5,))  # Normalize
    ])
    
    try:
        image = Image.open(image_path).convert("L")  # Convert to grayscale
        image = image.point(lambda p: p > 128 and 255)  # Binarization (thresholding)
        image = transform(image)
        image = image.unsqueeze(0)  # Add batch dimension
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")
    
    return image

