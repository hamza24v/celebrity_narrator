import React, { useRef, useEffect, useState } from 'react';

const CameraComponent = ({ onCapture }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [intervalId, setIntervalId] = useState(null);

  useEffect(() => {
    async function getMedia() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoRef.current.srcObject = stream;
      } catch (error) {
        console.error("Error accessing camera:", error);
      }
    }

    getMedia();
  }, []);

  const startCapturing = () => {
    const id = setInterval(() => {
      const context = canvasRef.current.getContext('2d');
      context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
      canvasRef.current.toBlob(blob => {
        const file = new File([blob], 'image.png', { type: 'image/jpeg' })
        console.log("Captured file:", file);
        onCapture(file);
      }, 'image/jpeg');
    }, 5000);
    setIntervalId(id);
  };

  const stopCapturing = () => {
    clearInterval(intervalId);
  };

  return (
    <div className="flex flex-col items-center">
      <video ref={videoRef} autoPlay className="w-full h-96"></video>
      <canvas ref={canvasRef} width="640" height="480" className="hidden"></canvas>
      <div className="mt-4">
        <button onClick={startCapturing} className=" bg-blue-500 text-white px-4 py-2 rounded mr-2">
          Start Narrating
        </button>
        <button onClick={stopCapturing} className=" bg-red-500 text-white px-4 py-2 rounded">
          Stop Narrating
        </button>
      </div>
    </div>
  );
};

export default CameraComponent;
