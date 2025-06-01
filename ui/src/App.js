import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { ThemeProvider, createTheme, styled } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Toolbar, Typography, Container, Card, CardContent, CardHeader, Button, CircularProgress, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField } from '@mui/material';
import axios from 'axios';

// Define the API URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:80';
// Define the MLflow UI URL (adjust based on deployment, e.g., Ngrok URL)
const MLFLOW_URL = process.env.REACT_APP_MLFLOW_URL || 'http://localhost:5000';

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

// Function to fetch logs
const getLogs = async (limit = 10) => {
  try {
    const response = await axios.get(`${API_URL}/logs?limit=${limit}`);
    return response.data.logs;
  } catch (error) {
    console.error('Error fetching logs:', error);
    throw error;
  }
};

// Define the MUI theme with dark mode and neon blue
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00D4FF',
    },
    secondary: {
      main: '#00B4D8',
    },
    background: {
      default: '#1A1F2E',
      paper: '#2A2F44',
    },
    text: {
      primary: '#E0E0E0',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.75rem',
      fontWeight: 700,
      color: '#00D4FF',
      textShadow: '0 0 10px rgba(0, 212, 255, 0.7), 0 0 5px rgba(0, 212, 255, 0.5)',
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

// Styled components for custom styling
const StyledCard = styled(Card)(({ theme }) => ({
  maxWidth: 600,
  width: '100%',
  margin: '20px auto',
  padding: theme.spacing(2),
  borderRadius: 12,
  backgroundColor: '#2A2F44',
  boxShadow: '0 0 15px rgba(0, 212, 255, 0.3), 0 0 5px rgba(0, 212, 255, 0.5)',
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
  const navigate = useNavigate();

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
              <StyledButton onClick={() => navigate('/')}>Home</StyledButton>
              <StyledButton onClick={() => navigate('/logs')}>View Logs</StyledButton>
            </Toolbar>
          </Container>
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="lg" sx={{ py: { xs: 2, sm: 4 } }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/results" element={<Results />} />
            <Route path="/logs" element={<Logs />} />
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
          {prediction && prediction.prediction !== undefined ? (
            <>
              <Typography variant="h6" gutterBottom sx={{ mb: 2, color: '#E0E0E0' }}>
                <strong>Prediction:</strong> {prediction.prediction}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                <strong>Confidence:</strong> {(prediction.confidence || 0).toFixed(2)}
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

// Logs Component
const Logs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [limit, setLimit] = useState(10);

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      try {
        const fetchedLogs = await getLogs(limit);
        setLogs(fetchedLogs);
      } catch (err) {
        setError('Error fetching logs: ' + (err.message || 'Check the server or MLflow.'));
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, [limit]);

  const handleLimitChange = (e) => {
    setLimit(parseInt(e.target.value) || 10);
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h1" gutterBottom sx={{ mt: { xs: 4, sm: 6 }, mb: 4 }}>
        Prediction Logs
      </Typography>
      <Box sx={{ mb: 2 }}>
        <TextField
          label="Number of Logs"
          variant="outlined"
          type="number"
          value={limit}
          onChange={handleLimitChange}
          sx={{ backgroundColor: '#1A1F2E', input: { color: '#E0E0E0' } }}
          InputProps={{ inputProps: { min: 1, max: 100 } }}
        />
      </Box>
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error" variant="body1" sx={{ textAlign: 'center', mt: 4 }}>
          {error}
        </Typography>
      ) : logs.length === 0 ? (
        <Typography variant="body1" sx={{ textAlign: 'center', mt: 4, color: '#B0B0B0' }}>
          No logs available.
        </Typography>
      ) : (
        <TableContainer component={Paper} sx={{ backgroundColor: '#2A2F44' }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ color: '#00D4FF', fontWeight: 600 }}>Run ID</TableCell>
                <TableCell sx={{ color: '#00D4FF', fontWeight: 600 }}>Filename</TableCell>
                <TableCell sx={{ color: '#00D4FF', fontWeight: 600 }}>Predicted Class</TableCell>
                <TableCell sx={{ color: '#00D4FF', fontWeight: 600 }}>Confidence</TableCell>
                <TableCell sx={{ color: '#00D4FF', fontWeight: 600 }}>Latency (s)</TableCell>
                <TableCell sx={{ color: '#00D4FF', fontWeight: 600 }}>Timestamp</TableCell>
                <TableCell sx={{ color: '#00D4FF', fontWeight: 600 }}>View in MLflow</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {logs.map((log) => (
                <TableRow key={log.run_id}>
                  <TableCell sx={{ color: '#E0E0E0' }}>{log.run_id.slice(0, 8)}</TableCell>
                  <TableCell sx={{ color: '#E0E0E0' }}>{log.filename}</TableCell>
                  <TableCell sx={{ color: '#E0E0E0' }}>{log.predicted_class}</TableCell>
                  <TableCell sx={{ color: '#E0E0E0' }}>{log.confidence.toFixed(2)}</TableCell>
                  <TableCell sx={{ color: '#E0E0E0' }}>{log.latency.toFixed(3)}</TableCell>
                  <TableCell sx={{ color: '#E0E0E0' }}>{log.timestamp}</TableCell>
                  <TableCell sx={{ color: '#E0E0E0' }}>
                    <a href={`${MLFLOW_URL}/#/experiments/0/runs/${log.run_id}`} target="_blank" rel="noopener noreferrer">
                      <StyledButton variant="contained" size="small">View</StyledButton>
                    </a>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Container>
  );
};

export default App;