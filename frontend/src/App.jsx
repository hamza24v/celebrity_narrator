import React, { useState, useEffect, useRef } from 'react';
import CameraComponent from './components/CameraComponent';
import { uploadImage, getAnalysis } from './services/narratorService';
import './index.css';
import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import Modal from './components/Modal';
import PauseCircleIcon from '@mui/icons-material/PauseCircle';
import ReplayIcon from '@mui/icons-material/Replay';

const App = () => {
  const [narration, setNarration] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const audioRef = useRef(new Audio());

  useEffect(() => {
    setShowModal(true);
  }, []);

  const handleCapture = async (imageData) => {
    setIsLoading(true);
    try {
      const uploadResponse = await uploadImage(imageData);
      const { id } = uploadResponse.data;
      const analysisResponse = await getAnalysis(id);
      setNarration(analysisResponse.data);
      audioRef.current.src = analysisResponse.data.audio_file // loads audio file
      analysisResponse.data.audio_file
    } catch (error) {
      console.error('Error capturing or analyzing image:', error);
    } finally {
      setIsLoading(false)
    }
  };

  const handlePlayAudio = () => {
    audioRef.current.play().catch(error => {
      console.error('Error playing audio:', error);
    });
  };

  const handlePauseAudio = () => {
    audioRef.current.pause();
  };

  const handleRestartAudio = () => {
    audioRef.current.currentTime = 0;
    audioRef.current.play().catch(error => {
      console.error('Error playing audio:', error);
    });
  };
  return (
    <main>
      <div className='main'>
        <div className='gradient' />
      </div>
      <div className="flex justify-center items-center flex-col max-w-7xl mx-auto sm:px-16 px-6 relative z-10">
        <h1 className="my-5 text-4xl font-bold leading-[1.15] text-black sm:text-5xl text-center;">
          David Attenborough <span className='orange_gradient'>Narrates!</span></h1>
        <CameraComponent onCapture={handleCapture} />
        <div className='max-w-full flex justify-center items-center'>
          {isLoading ? (
            <img src='./src/assets/loader.svg' alt='loader' className='my-20 size-20 object-contain' />
          ) :
            (
              narration && (
                <div className="grid grid-col justify-items-center mt-4 p-4 border rounded bg-gray-100">
                  <div className='summary_box'>
                    <p className='font-inter font-medium text-sm text-gray-700'>
                      {narration.analysis}
                    </p>
                  </div>
                  <div className="flex justify-center space-x-4">
                    <button onClick={handlePlayAudio}>
                      <PlayCircleIcon style={{ fontSize: 50 }} />
                    </button>
                    <button onClick={handlePauseAudio}>
                      <PauseCircleIcon style={{ fontSize: 50 }} />
                    </button>
                    <button onClick={handleRestartAudio}>
                      <ReplayIcon style={{ fontSize: 50 }} />
                    </button>
                  </div>
                </div>
              ))}
        </div>
        <Modal showModal={showModal} setShowModal={setShowModal} />
      </div>
    </main>

  );
};

export default App;
