import React from 'react';

const Modal = ({ showModal, setShowModal }) => {
  if (!showModal) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      <div className="fixed inset-0 bg-black opacity-50"></div>
      <div className="bg-white p-6 rounded-lg shadow-lg z-10">
        <h2 className="text-2xl font-bold mb-4 text-black">Welcome to David Attenborough Narrates!</h2>
        <p className="mb-4 text-black max-w-lg">Ever dreamed of having David Attenborough narrate your 
            daily life? Your wish is now a reality! Follow these simple steps:</p>
        <ol className="list-decimal list-inside mb-4 text-black">
          <li>Allow access to your webcam.</li>
          <li>Click "Take a snapshot to narrate"</li>
          <li>Enjoy the personalized narration.</li>
        </ol>
        <button
          onClick={() => setShowModal(false)}
          className="px-4 py-2 bg-orange-500 text-gray-200 rounded hover:bg-orange-600"
        >
          Got it!
        </button>
      </div>
    </div>
  );
};

export default Modal;
