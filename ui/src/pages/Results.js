import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Card, CardContent, Typography, Container } from '@mui/material';

const Results = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const prediction = state?.prediction || {};

  return (
    <Container>
      <Typography variant="h1" gutterBottom sx={{ mt: 4, mb: 2 }}>
        Résultats de la Prédiction
      </Typography>
      <Card sx={{ maxWidth: 600, margin: '20px auto', padding: 2 }}>
        <CardContent>
          {prediction && prediction.prediction ? (
            <>
              <Typography variant="h6" gutterBottom>
                <strong>Prédiction :</strong> {prediction.prediction}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Message :</strong> {prediction.message || 'Non disponible'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Fichier :</strong> {prediction.filename || 'Non disponible'}
              </Typography>
            </>
          ) : (
            <Typography color="text.secondary">
              Aucune prédiction disponible. Veuillez réessayer.
            </Typography>
          )}
          <Button
            variant="outlined"
            color="primary"
            onClick={() => navigate('/')}
            sx={{ mt: 2 }}
          >
            Retour à l'accueil
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Results;