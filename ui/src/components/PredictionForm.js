import React, { useState } from 'react';
import { getPrediction } from '../api/api';
import { Button, Card, CardContent, CardHeader, CircularProgress, Typography } from '@mui/material';

const PredictionForm = ({ onPrediction }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Veuillez sélectionner un fichier.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await getPrediction(file);
      if (!result || !result.prediction) {
        throw new Error('Réponse invalide du serveur: aucune prédiction reçue.');
      }
      onPrediction(result);
    } catch (err) {
      console.error('Error during prediction:', err);
      setError('Erreur lors de la prédiction: ' + (err.message || 'Vérifiez le serveur.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ maxWidth: 600, margin: '20px auto', padding: 2 }}>
      <CardHeader title="Uploader une image" />
      <CardContent>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ marginBottom: '16px' }}
            disabled={loading}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            startIcon={loading && <CircularProgress size={20} />}
          >
            {loading ? 'Traitement...' : 'Prédire'}
          </Button>
        </form>
        {error && (
          <Typography color="error" variant="body2" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default PredictionForm;