from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import numpy as np
from pathlib import Path
import tempfile
import logging
import nibabel as nib
import pydicom
from monai.networks.nets import UNet
from monai.inferers import SlidingWindowInferer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MedImaging Segmentation", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Device: {device}")

MODELS = {
    "liver": {"name": "Liver Segmentation"},
    "lung": {"name": "Lung Segmentation"},
    "spleen": {"name": "Spleen Segmentation"},
}

model_cache = {}

# HTML UI
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedImaging Segmentation</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: rgba(0, 0, 0, 0.2);
            color: white;
            padding: 3rem 1rem;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .container {
            flex: 1;
            max-width: 600px;
            margin: 2rem auto;
            width: 100%;
            padding: 0 1rem;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .card h2 { color: #333; font-size: 1.3rem; margin-bottom: 1rem; }
        .dropzone {
            border: 3px dashed #667eea;
            border-radius: 8px;
            padding: 3rem 1rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f5f7fa;
        }
        .dropzone:hover { border-color: #764ba2; background: #eff5ff; }
        .dropzone.drag { border-color: #764ba2; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .dropzone-icon { font-size: 3rem; margin-bottom: 1rem; }
        .dropzone-text { font-size: 1.1rem; color: #333; font-weight: 500; margin-bottom: 0.5rem; }
        .model-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }
        .model-button {
            padding: 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }
        .model-button:hover { border-color: #667eea; background: #f5f7fa; }
        .model-button.active { border-color: #667eea; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .segment-button {
            width: 100%;
            padding: 1.2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 1rem;
        }
        .segment-button:hover { transform: translateY(-2px); }
        .segment-button:disabled { opacity: 0.6; cursor: not-allowed; }
        .result { background: #e8f5e9; border: 2px solid #4caf50; border-radius: 12px; padding: 2rem; text-align: center; }
        .error { background: #ffebee; border: 2px solid #ef5350; border-radius: 12px; padding: 1.5rem; color: #c62828; margin-bottom: 1rem; }
        .footer {
            background: rgba(0, 0, 0, 0.2);
            color: white;
            text-align: center;
            padding: 2rem;
            backdrop-filter: blur(10px);
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>MedImaging Segmentation</h1>
        <p>AI-powered medical image segmentation in seconds</p>
    </header>

    <main class="container">
        <div class="card">
            <h2>1. Upload Image</h2>
            <div class="dropzone" id="dropzone">
                <div class="dropzone-icon">📁</div>
                <p class="dropzone-text" id="dropzone-text">Drag & drop your DICOM or NIFTI file here</p>
                <p class="dropzone-subtext">or click to select</p>
                <input type="file" id="file-input" style="display:none;" accept=".dcm,.nii,.nii.gz">
            </div>
        </div>

        <div class="card">
            <h2>2. Select Model</h2>
            <div class="model-grid">
                <button class="model-button active" data-model="liver">🫀 Liver</button>
                <button class="model-button" data-model="lung">🫁 Lung</button>
                <button class="model-button" data-model="spleen">💜 Spleen</button>
            </div>
        </div>

        <button class="segment-button" id="segment-btn" disabled>3. Segment Image</button>
        <div id="error-container"></div>
        <div id="result-container"></div>
    </main>

    <footer class="footer">
        <p>Fast, accurate medical image segmentation powered by AI</p>
    </footer>

    <script>
        let selectedFile = null;
        let selectedModel = 'liver';

        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('file-input');
        const segmentBtn = document.getElementById('segment-btn');
        const errorContainer = document.getElementById('error-container');
        const resultContainer = document.getElementById('result-container');
        const dropzoneText = document.getElementById('dropzone-text');

        dropzone.addEventListener('click', () => fileInput.click());
        dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('drag'); });
        dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag'));
        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('drag');
            if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) handleFile(e.target.files[0]);
        });

        function handleFile(file) {
            selectedFile = file;
            dropzoneText.textContent = file.name;
            segmentBtn.disabled = false;
            errorContainer.innerHTML = '';
            resultContainer.innerHTML = '';
        }

        document.querySelectorAll('.model-button').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.model-button').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                selectedModel = this.dataset.model;
            });
        });

        segmentBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
            
            segmentBtn.disabled = true;
            errorContainer.innerHTML = '';
            resultContainer.innerHTML = '';

            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('model_name', selectedModel);

            try {
                const response = await fetch('/segment', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error('Segmentation failed');

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                
                resultContainer.innerHTML = `
                    <div class="result">
                        <h3>✓ Segmentation Complete!</h3>
                        <p>Your segmentation is ready to download.</p>
                        <button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; border: none; border-radius: 8px; cursor: pointer; margin-top: 1rem;" onclick="downloadFile('${url}', 'segmentation.nii.gz')">Download Result</button>
                    </div>
                `;
            } catch (err) {
                errorContainer.innerHTML = `<div class="error">❌ ${err.message}</div>`;
            } finally {
                segmentBtn.disabled = false;
            }
        });

        function downloadFile(url, name) {
            const link = document.createElement('a');
            link.href = url;
            link.download = name;
            link.click();
        }
    </script>
</body>
</html>"""

def get_model(model_name: str):
    if model_name in model_cache:
        return model_cache[model_name]
    if model_name not in MODELS:
        raise HTTPException(status_code=400, detail=f"Unknown model: {model_name}")
    logger.info(f"Creating {model_name} model...")
    model = UNet(spatial_dims=3, in_channels=1, out_channels=2, channels=(16, 32, 64, 128), strides=(2, 2, 2), num_res_units=2)
    model = model.to(device)
    model.eval()
    model_cache[model_name] = model
    return model

def load_medical_image(path: Path) -> np.ndarray:
    try:
        if path.suffix.lower() == '.dcm':
            ds = pydicom.dcmread(path)
            img = ds.pixel_array.astype(np.float32)
            if len(img.shape) == 2:
                img = np.expand_dims(img, axis=0)
        else:
            nifti = nib.load(path)
            img = nifti.get_fdata().astype(np.float32)
        img = (img - img.min()) / (img.max() - img.min() + 1e-8)
        return img
    except Exception as e:
        logger.error(f"Load error: {e}")
        raise HTTPException(status_code=400, detail="Invalid image file")

def segment_image(img: np.ndarray, model) -> np.ndarray:
    try:
        if len(img.shape) == 3:
            img = np.expand_dims(img, axis=0)
        tensor = torch.from_numpy(img).unsqueeze(0).to(device)
        with torch.no_grad():
            inferer = SlidingWindowInferer(roi_size=(64, 64, 64), sw_batch_size=4, overlap=0.5)
            pred = inferer(tensor, model)
        seg = torch.argmax(pred, dim=1).squeeze().cpu().numpy().astype(np.uint8)
        return seg
    except Exception as e:
        logger.error(f"Segmentation error: {e}")
        raise HTTPException(status_code=500, detail="Segmentation failed")

@app.get("/", response_class=HTMLResponse)
def root():
    return HTML_CONTENT

@app.get("/api")
def api_status():
    return {"api": "MedImaging Segmentation", "status": "running"}

@app.get("/models")
def list_models():
    return {"models": [{"id": k, "name": v["name"]} for k, v in MODELS.items()]}

@app.post("/segment")
async def segment(file: UploadFile = File(...), model_name: str = Query("liver")):
    tmpdir = Path(tempfile.mkdtemp())
    try:
        input_path = tmpdir / file.filename
        with open(input_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"Processing {file.filename} with {model_name}")
        img = load_medical_image(input_path)
        model = get_model(model_name)
        seg = segment_image(img, model)
        output = tmpdir / "result.nii.gz"
        nib.save(nib.Nifti1Image(seg, np.eye(4)), output)
        logger.info(f"Segmentation complete: {seg.shape}")
        return FileResponse(output, filename="segmentation.nii.gz")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

@app.get("/health")
def health():
    return {"status": "ok", "device": str(device)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
