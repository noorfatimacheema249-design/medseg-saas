# MedImaging Segmentation - SaaS

Fast, accurate medical image segmentation powered by AI. Built for radiologists and hospitals.

## Features

- 🚀 **Fast**: Process DICOM/NIFTI files in seconds
- 🧠 **AI-Powered**: State-of-the-art deep learning segmentation
- 🖥️ **No Installation**: Web-based, zero setup required
- 🔒 **Private**: Process on your own infrastructure
- 💰 **Affordable**: Pay per segmentation or monthly subscription

## Supported Models

- **Liver Segmentation**: CT liver segmentation with 95%+ accuracy
- **Lung Segmentation**: CT lung segmentation for nodule detection
- **Spleen Segmentation**: CT spleen segmentation for trauma assessment

## Quick Start

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm start
```

Visit `http://localhost:3000`

### Docker

```bash
cd docker
docker-compose up
```

## API Usage

```bash
curl -X POST "http://localhost:8000/segment" \
  -F "file=@scan.dcm" \
  -F "model_name=liver" \
  --output result.nii.gz
```

## Deployment

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Connect this repo
3. Set `DOCKERFILE` as the runtime
4. Deploy!

### AWS/Azure/GCP

```bash
docker build -f docker/Dockerfile -t medseg .
docker run -p 8000:8000 medseg
```

## Pricing

- **Free Tier**: 5 segmentations/month
- **Pro**: $99/month (unlimited segmentations)
- **Enterprise**: Custom pricing (1000+ segmentations/month)

## Architecture

```
Frontend (React)
     ↓
  API (FastAPI)
     ↓
Models (MONAI/PyTorch)
     ↓
Medical Images (DICOM/NIFTI)
```

## File Structure

```
medseg-saas/
├── backend/
│   ├── main.py          # FastAPI application
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── App.jsx          # React component
│   ├── App.css          # Styling
│   ├── package.json     # Dependencies
│   └── public/
│       └── index.html
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

## API Endpoints

- `GET /` - API status
- `GET /models` - List available models
- `GET /health` - Health check
- `POST /segment` - Run segmentation (form data: file, model_name)

## Requirements

- Python 3.11+
- PyTorch 2.0+
- Node.js 18+
- 8GB RAM minimum
- GPU recommended (NVIDIA CUDA)

## License

MIT

## Support

For issues or questions, open a GitHub issue or email support@medseg.app

---

**Made with ❤️ for radiologists and medical professionals**
