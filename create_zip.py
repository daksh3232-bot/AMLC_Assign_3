import zipfile
import os

files_to_zip = [
    'Report.pdf',
    'Dockerfile.train',
    'Dockerfile.inference',
    'pvc.yaml',
    'train-job.yaml',
    'inference-deployment.yaml',
    'inference-service.yaml',
    'train.py',
    'app.py'
]

zip_name = 'Assign_3_da3232.zip'

with zipfile.ZipFile(zip_name, 'w') as zipf:
    for file in files_to_zip:
        if os.path.exists(file):
            zipf.write(file)
            print(f"Added {file}")
        else:
            print(f"Warning: {file} not found")

print(f"Successfully created {zip_name}")
