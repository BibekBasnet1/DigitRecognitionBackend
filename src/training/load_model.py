import os
import torch
from src.training.model import DigitCNN

def load_trained_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    model_path = os.path.join(base_dir, 'third_model.pth')  

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = DigitCNN()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    return model
