import React from 'react';
import PredictionForm from '../components/PredictionForm';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handlePrediction = (result) => {
    navigate('/results', { state: { prediction: result } }); // Redirige vers la page de résultats
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Détection de l'Alzheimer</h1>
      <p>Chargez une image pour obtenir une prédiction.</p>
      <PredictionForm onPrediction={handlePrediction} />
    </div>
  );
};

export default Home;