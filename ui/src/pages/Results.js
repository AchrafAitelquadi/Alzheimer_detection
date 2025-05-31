import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';

const Results = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const prediction = state?.prediction || {};

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Résultats de la Prédiction</h1>
      {prediction ? (
        <div>
          <p><strong>Prédiction :</strong> {prediction.prediction || 'Non disponible'}</p>
          <p><strong>Message :</strong> {prediction.message || 'Non disponible'}</p>
          <p><strong>Fichier :</strong> {prediction.filename || 'Non disponible'}</p>
        </div>
      ) : (
        <p>Aucune prédiction disponible.</p>
      )}
      <Button variant="outlined" onClick={() => navigate('/')}>
        Retour à l'accueil
      </Button>
    </div>
  );
};

export default Results;