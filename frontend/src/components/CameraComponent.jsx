import React, { useRef, useEffect, useState } from 'react';

const CameraComponent = ({ onCapture }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [flash, setFlash] = useState(false)
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

  const takeSnapshot = () => {
    playSnapshotSound()
    const context = canvasRef.current.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
    canvasRef.current.toBlob(blob => {
      const file = new File([blob], 'image.png', { type: 'image/jpeg' })
      onCapture(file);
      triggerFlash()
    }, 'image/jpeg');
  };

  const playSnapshotSound = () => {
    const sound = document.getElementById('snapshotSound');
    sound.play();
  };

  const triggerFlash = () => {
    setFlash(true);
    setTimeout(() => setFlash(false), 100);
  };


  return (
    <div className="flex flex-col items-center">
      <video ref={videoRef} autoPlay className="w-full h-96"></video>
      <canvas ref={canvasRef} width="640" height="480" className="hidden"></canvas>
      <button onClick={takeSnapshot} className=" bg-orange-400  px-4 py-2 rounded mr-2 mt-5 text-lg text-gray-200 sm:text-xl text-center max-w-2xl">
        Take a snapshot to narrate
      </button>
      {flash && <div className="absolute top-0 left-0 w-full h-full bg-white opacity-50 animate-flash"></div>}
    </div>
  );
};

export default CameraComponent;
