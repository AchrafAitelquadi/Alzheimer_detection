import React, { useState } from 'react';
import { getPrediction } from '../api/api';
import { Button, TextField, CircularProgress } from '@mui/material';

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
      onPrediction(result); // Transmet le résultat à la page parent
    } catch (err) {
      setError('Erreur lors de la prédiction. Vérifiez votre fichier ou le serveur.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <TextField
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          inputProps={{ accept: 'image/*' }} // Limite aux images
          disabled={loading}
        />
        <Button type="submit" variant="contained" color="primary" disabled={loading}>
          {loading ? <CircularProgress size={24} /> : 'Prédire'}
        </Button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default PredictionForm;