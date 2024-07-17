import React, { useState } from 'react';
import CameraComponent from './components/CameraComponent';
import { uploadImage, getAnalysis } from './services/narratorService';
import './index.css'; 

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
    <div className="flex flex-col h-screen justify-center items-center">
    <h1 className="text-4xl font-bold text-center mb-10">Celebrity Narrator</h1>
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
