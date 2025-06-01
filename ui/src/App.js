import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { ThemeProvider, createTheme, styled } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Toolbar, Typography, Container, Card, CardContent, CardHeader, Button, CircularProgress, Box } from '@mui/material';
import axios from 'axios';

// Define the API URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:80';

// Function to make prediction API call
const getPrediction = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await axios.post(`${API_URL}/predict`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    console.log('Backend Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching prediction:', error);
    throw error;
  }
};

// Define the MUI theme with dark mode and neon blue (without self-reference)
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00D4FF', // Neon blue
    },
    secondary: {
      main: '#00B4D8', // Slightly darker neon blue
    },
    background: {
      default: '#1A1F2E', // Dark background
      paper: '#2A2F44', // Slightly lighter for cards
    },
    text: {
      primary: '#E0E0E0', // Light gray for readability
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.75rem',
      fontWeight: 700,
      color: '#00D4FF',
      textShadow: '0 0 10px rgba(0, 212, 255, 0.7), 0 0 5px rgba(0, 212, 255, 0.5)', // Neon text glow
      textAlign: 'center',
    },
    h6: {
      fontSize: '1.25rem',
      fontWeight: 600,
      color: '#B0B0B0',
    },
    body1: {
      fontSize: '1.1rem',
      color: '#CCCCCC',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#2A2F44',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1A1F2E',
          boxShadow: '0 0 15px rgba(0, 212, 255, 0.3)',
        },
      },
    },
  },
});

// Styled components for custom styling (defined after theme)
const StyledCard = styled(Card)(({ theme }) => ({
  maxWidth: 600,
  width: '100%',
  margin: '20px auto',
  padding: theme.spacing(2),
  borderRadius: 12,
  backgroundColor: '#2A2F44',
  boxShadow: '0 0 15px rgba(0, 212, 255, 0.3), 0 0 5px rgba(0, 212, 255, 0.5)', // Neon glow effect
  transition: 'transform 0.2s',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 0 20px rgba(0, 212, 255, 0.5), 0 0 10px rgba(0, 212, 255, 0.7)',
  },
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(1.5),
    margin: '10px auto',
  },
}));

const StyledButton = styled(Button)(({ theme }) => ({
  borderRadius: 8,
  padding: theme.spacing(1, 2),
  backgroundColor: '#00D4FF',
  color: '#1A1F2E',
  textTransform: 'none',
  fontWeight: 600,
  transition: 'all 0.3s',
  '&:hover': {
    backgroundColor: '#00B4D8',
    boxShadow: '0 0 10px rgba(0, 212, 255, 0.7)',
    color: '#FFFFFF',
  },
  '&:disabled': {
    backgroundColor: '#555555',
    color: '#CCCCCC',
  },
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(0.75, 1.5),
    fontSize: '0.875rem',
  },
}));

const DropZone = styled('div')(({ theme }) => ({
  border: '2px dashed #00D4FF',
  borderRadius: 8,
  padding: theme.spacing(5),
  textAlign: 'center',
  backgroundColor: '#1A1F2E',
  cursor: 'pointer',
  transition: 'all 0.3s',
  boxShadow: 'inset 0 0 10px rgba(0, 212, 255, 0.2)',
  '&:hover': {
    borderColor: '#00B4D8',
    boxShadow: 'inset 0 0 15px rgba(0, 212, 255, 0.4)',
  },
  '&.dragover': {
    borderColor: '#00B4D8',
    backgroundColor: '#2A2F44',
    boxShadow: 'inset 0 0 20px rgba(0, 212, 255, 0.5)',
  },
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(3),
  },
}));

// Main App Component
const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        {/* Header */}
        <AppBar position="static" color="primary" elevation={4}>
          <Container maxWidth="lg">
            <Toolbar sx={{ minHeight: { xs: 48, sm: 64 } }}>
              <Typography
                variant="h6"
                component="div"
                sx={{
                  flexGrow: 1,
                  fontWeight: 700,
                  color: '#00D4FF',
                  textShadow: '0 0 5px rgba(0, 212, 255, 0.7)',
                  fontSize: { xs: '1.1rem', sm: '1.25rem' },
                }}
              >
                Alzheimer Detection System
              </Typography>
            </Toolbar>
          </Container>
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="lg" sx={{ py: { xs: 2, sm: 4 } }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/results" element={<Results />} />
          </Routes>
        </Container>
      </Router>
    </ThemeProvider>
  );
};

// Home Component (Prediction Form with Drag-and-Drop)
const Home = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith('image/')) {
      setFile(droppedFile);
    } else {
      setError('Please drop a valid image file.');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select or drop an image file.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await getPrediction(file);
      if (!result || !result.prediction) {
        throw new Error('Invalid server response: no prediction received.');
      }
      console.log('Result before navigation:', result);
      navigate('/results', { state: { prediction: result } });
    } catch (err) {
      console.error('Error during prediction:', err);
      setError('Error during prediction: ' + (err.message || 'Check the server.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h1" gutterBottom sx={{ mt: { xs: 4, sm: 6 }, mb: 4 }}>
        Alzheimer Detection
      </Typography>
      <Typography variant="body1" paragraph sx={{ mb: 4, textAlign: 'center' }}>
        Welcome! Upload a medical image to get an AI-assisted prediction for Alzheimer detection.
      </Typography>
      <StyledCard>
        <CardHeader title="Upload Image" sx={{ pb: 0, color: '#00D4FF' }} />
        <CardContent>
          <DropZone
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={dragOver ? 'dragover' : ''}
          >
            <Typography variant="body1" sx={{ mb: 2, color: '#B0B0B0' }}>
              Drag and drop an image here, or click to select one.
            </Typography>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ display: 'none' }}
              id="file-input"
            />
            <label htmlFor="file-input">
              <StyledButton variant="contained" color="primary" component="span">
                Select Image
              </StyledButton>
            </label>
          </DropZone>
          <Box sx={{ mt: 2 }}>
            <StyledButton
              type="submit"
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              disabled={loading || !file}
              startIcon={loading && <CircularProgress size={20} />}
              sx={{ width: '100%' }}
            >
              {loading ? 'Processing...' : 'Predict'}
            </StyledButton>
          </Box>
          {error && (
            <Typography color="error" variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
              {error}
            </Typography>
          )}
        </CardContent>
      </StyledCard>
    </Container>
  );
};

// Results Component
const Results = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const prediction = state?.prediction || {};

  return (
    <Container maxWidth="md">
      <Typography variant="h1" gutterBottom sx={{ mt: { xs: 4, sm: 6 }, mb: 4 }}>
        Prediction Results
      </Typography>
      <StyledCard>
        <CardContent>
          {prediction && prediction.prediction ? (
            <>
              <Typography variant="h6" gutterBottom sx={{ mb: 2, color: '#E0E0E0' }}>
                <strong>Prediction:</strong> {prediction.prediction}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                <strong>Message:</strong> {prediction.message || 'Not available'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>File:</strong> {prediction.filename || 'Not available'}
              </Typography>
            </>
          ) : (
            <Typography color="text.secondary" sx={{ mb: 2 }}>
              No prediction available. Please try again.
            </Typography>
          )}
          <StyledButton
            variant="outlined"
            color="primary"
            onClick={() => navigate('/')}
            sx={{ mt: 3, width: '100%' }}
          >
            Back to Home
          </StyledButton>
        </CardContent>
      </StyledCard>
    </Container>
  );
};

export default App;