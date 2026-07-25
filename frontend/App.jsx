import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [model, setModel] = useState('liver');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setError(null);
      setResult(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/dicom': ['.dcm'],
      'application/x-nifti-gz': ['.nii.gz'],
      'application/x-nifti': ['.nii']
    }
  });

  const handleSegment = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    setProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('model_name', model);

      const response = await axios.post(`${API_URL}/segment`, formData, {
        responseType: 'blob',
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 30) / progressEvent.total
          );
          setProgress(percentCompleted);
        }
      });

      setProgress(100);
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setResult({
        url,
        filename: 'segmentation.nii.gz',
        success: true
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Segmentation failed. Check file format and try again.'
      );
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (result?.url) {
      const link = document.createElement('a');
      link.href = result.url;
      link.download = result.filename;
      link.click();
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError(null);
    setProgress(0);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>MedImaging Segmentation</h1>
        <p>AI-powered medical image segmentation in seconds</p>
      </header>

      <main className="container">
        {/* Upload Area */}
        <div className="card">
          <h2>1. Upload Image</h2>
          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
          >
            <input {...getInputProps()} />
            {!file ? (
              <>
                <div className="dropzone-icon">📁</div>
                <p className="dropzone-text">Drag & drop your DICOM or NIFTI file here</p>
                <p className="dropzone-subtext">or click to select</p>
              </>
            ) : (
              <>
                <div className="dropzone-icon">✓</div>
                <p className="dropzone-text">{file.name}</p>
                <p className="dropzone-subtext">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </>
            )}
          </div>
        </div>

        {/* Model Selection */}
        <div className="card">
          <h2>2. Select Model</h2>
          <div className="model-grid">
            {['liver', 'lung', 'spleen'].map(m => (
              <button
                key={m}
                className={`model-button ${model === m ? 'active' : ''}`}
                onClick={() => setModel(m)}
                disabled={loading}
              >
                <span className="model-name">
                  {m.charAt(0).toUpperCase() + m.slice(1)}
                </span>
                <span className="model-icon">
                  {m === 'liver' && '🫀'}
                  {m === 'lung' && '🫁'}
                  {m === 'spleen' && '💜'}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Segmentation Button */}
        <button
          className="segment-button"
          onClick={handleSegment}
          disabled={!file || loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Segmenting... {progress}%
            </>
          ) : (
            '3. Segment Image'
          )}
        </button>

        {/* Progress Bar */}
        {loading && (
          <div className="progress-container">
            <div className="progress-bar" style={{ width: `${progress}%` }}></div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="error-card">
            <span className="error-icon">❌</span>
            <p>{error}</p>
            <button onClick={() => setError(null)} className="close-error">×</button>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="result-card">
            <div className="result-icon">✓</div>
            <h3>Segmentation Complete!</h3>
            <p>Your segmentation is ready to download.</p>
            <div className="result-buttons">
              <button className="download-button" onClick={handleDownload}>
                Download Result
              </button>
              <button className="reset-button" onClick={handleReset}>
                Process Another
              </button>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Fast, accurate medical image segmentation powered by AI</p>
      </footer>
    </div>
  );
}

export default App;
