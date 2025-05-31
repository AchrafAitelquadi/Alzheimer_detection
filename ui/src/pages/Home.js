import React from 'react';
import PredictionForm from '../components/PredictionForm';
import { useNavigate } from 'react-router-dom';
import { Typography, Container } from '@mui/material';

const Home = () => {
  const navigate = useNavigate();

  const handlePrediction = (result) => {
    console.log('Result before navigation:', result);
    navigate('/results', { state: { prediction: result } });
  };

  return (
    <Container>
      <Typography variant="h1" gutterBottom sx={{ mt: 4, mb: 2 }}>
        Détection de l'Alzheimer
      </Typography>
      <Typography variant="body1" paragraph>
        Bienvenue ! Chargez une image médicale pour obtenir une prédiction assistée par intelligence artificielle concernant la détection de l'Alzheimer.
      </Typography>
      <PredictionForm onPrediction={handlePrediction} />
    </Container>
  );
};

export default Home;