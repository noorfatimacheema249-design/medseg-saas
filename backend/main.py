"""
FastAPI backend for medical imaging segmentation
Upload DICOM/NIFTI → Segment → Download result
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import numpy as np
from pathlib import Path
import tempfile
import logging

# Medical imaging
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
    "liver": {"name": "Liver Segmentation", "desc": "CT liver segmentation"},
    "lung": {"name": "Lung Segmentation", "desc": "CT lung segmentation"},
    "spleen": {"name": "Spleen Segmentation", "desc": "CT spleen segmentation"},
}

model_cache = {}


def get_model(model_name: str):
    """Get or create model"""
    if model_name in model_cache:
        return model_cache[model_name]
    
    if model_name not in MODELS:
        raise HTTPException(status_code=400, detail=f"Unknown model: {model_name}")
    
    logger.info(f"Creating {model_name} model...")
    model = UNet(
        spatial_dims=3,
        in_channels=1,
        out_channels=2,
        channels=(16, 32, 64, 128),
        strides=(2, 2, 2),
        num_res_units=2,
    )
    model = model.to(device)
    model.eval()
    model_cache[model_name] = model
    return model


def load_medical_image(path: Path) -> np.ndarray:
    """Load DICOM or NIFTI file"""
    try:
        if path.suffix.lower() == '.dcm':
            ds = pydicom.dcmread(path)
            img = ds.pixel_array.astype(np.float32)
            if len(img.shape) == 2:
                img = np.expand_dims(img, axis=0)
        else:  # NIFTI
            nifti = nib.load(path)
            img = nifti.get_fdata().astype(np.float32)
        
        # Normalize
        img = (img - img.min()) / (img.max() - img.min() + 1e-8)
        return img
    except Exception as e:
        logger.error(f"Load error: {e}")
        raise HTTPException(status_code=400, detail="Invalid image file")


def segment_image(img: np.ndarray, model) -> np.ndarray:
    """Run segmentation"""
    try:
        if len(img.shape) == 3:
            img = np.expand_dims(img, axis=0)
        
        tensor = torch.from_numpy(img).unsqueeze(0).to(device)
        
        with torch.no_grad():
            inferer = SlidingWindowInferer(
                roi_size=(64, 64, 64),
                sw_batch_size=4,
                overlap=0.5
            )
            pred = inferer(tensor, model)
        
        seg = torch.argmax(pred, dim=1).squeeze().cpu().numpy().astype(np.uint8)
        return seg
    except Exception as e:
        logger.error(f"Segmentation error: {e}")
        raise HTTPException(status_code=500, detail="Segmentation failed")


@app.get("/")
def root():
    return {"api": "MedImaging Segmentation", "status": "running"}


@app.get("/models")
def list_models():
    return {"models": [{"id": k, "name": v["name"]} for k, v in MODELS.items()]}


@app.post("/segment")
async def segment(
    file: UploadFile = File(...),
    model_name: str = Query("liver")
):
    """Upload image → Segment → Download"""
    tmpdir = Path(tempfile.mkdtemp())
    
    try:
        # Save upload
        input_path = tmpdir / file.filename
        with open(input_path, "wb") as f:
            f.write(await file.read())
        
        logger.info(f"Processing {file.filename} with {model_name}")
        
        # Load → Segment
        img = load_medical_image(input_path)
        model = get_model(model_name)
        seg = segment_image(img, model)
        
        # Save result
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
