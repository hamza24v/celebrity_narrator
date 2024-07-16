import React, { useState } from 'react';
import CameraComponent from './components/CameraComponent';
import { uploadImage, getAnalysis } from './services/narratorService';
import './index.css'; // Ensure Tailwind CSS is imported

const App = () => {
  const [narration, setNarration] = useState(null);

  const handleCapture = async (imageData) => {
    try {
      const uploadResponse = await uploadImage(imageData);
      const { id } = uploadResponse.data;
      const analysisResponse = await getAnalysis(id);
      setNarration(analysisResponse.data);
    } catch (error) {
      console.error('Error capturing or analyzing image:', error);
    }
  };

  return (
    <div className="mx-auto p-4">
    <h1 className="text-3xl font-bold text-center my-4">Narrator</h1>
    <CameraComponent onCapture={handleCapture} />
    {narration && (
      <div className="analysis-result mt-4 p-4 border rounded bg-gray-100">
        <p className="mb-4">{narration.analysis}</p>
        <audio controls src={narration.audio_file}></audio>
      </div>
    )}
  </div>
  );
};

export default App;
