from flask import Flask, request, render_template, jsonify
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io
import os

app = Flask(__name__)

# Define the same MLP architecture
class SimpleMLP(nn.Module):
    def __init__(self):
        super(SimpleMLP, self).__init__()
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        return self.fc(x)

model = None
model_path = "/mnt/model/model.pth"

def load_model():
    global model
    if os.path.exists(model_path):
        model = SimpleMLP()
        # Explicitly map to CPU to avoid using the 1 available GPU
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()
        print("Model loaded successfully on CPU.")
    else:
        print(f"Model not found at {model_path}. Please run training first.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    img = Image.open(io.BytesIO(file.read())).convert('L')
    img = img.resize((28, 28))
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    img_tensor = transform(img).unsqueeze(0)
    
    with torch.no_grad():
        output = model(img_tensor)
        prediction = output.argmax(dim=1, keepdim=True).item()
    
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=5000)
