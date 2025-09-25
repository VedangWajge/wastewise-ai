import React, { useState, useRef, useCallback } from 'react';
import './Camera.css';

const Camera = ({ onImageCapture }) => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const startCamera = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'environment' // Use back camera on mobile
        }
      });

      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        setIsStreaming(true);
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
      setError('Unable to access camera. Please check permissions.');
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => {
        track.stop();
      });
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsStreaming(false);
  }, []);

  const captureImage = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob && onImageCapture) {
        const file = new File([blob], `waste-image-${Date.now()}.jpg`, {
          type: 'image/jpeg'
        });
        onImageCapture(file);
      }
    }, 'image/jpeg', 0.8);

    stopCamera();
  }, [onImageCapture, stopCamera]);

  const handleFileUpload = useCallback((event) => {
    const file = event.target.files[0];
    if (file && onImageCapture) {
      onImageCapture(file);
    }
  }, [onImageCapture]);

  return (
    <div className="camera-container">
      <div className="camera-header">
        <h2>Capture Waste Image</h2>
        <p>Take a photo or upload an image for classification</p>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      <div className="camera-section">
        {!isStreaming ? (
          <div className="camera-controls">
            <button
              className="btn btn-primary"
              onClick={startCamera}
            >
              📸 Start Camera
            </button>
            <div className="upload-section">
              <label htmlFor="file-upload" className="btn btn-secondary">
                📁 Upload Image
              </label>
              <input
                id="file-upload"
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
            </div>
          </div>
        ) : (
          <div className="camera-view">
            <video
              ref={videoRef}
              className="video-stream"
              autoPlay
              playsInline
              muted
            />
            <div className="camera-actions">
              <button
                className="btn btn-success"
                onClick={captureImage}
              >
                📷 Capture
              </button>
              <button
                className="btn btn-danger"
                onClick={stopCamera}
              >
                ❌ Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      <canvas
        ref={canvasRef}
        style={{ display: 'none' }}
      />
    </div>
  );
};

export default Camera;