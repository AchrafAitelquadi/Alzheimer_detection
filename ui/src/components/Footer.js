import React from 'react';
import { Container, Typography } from '@mui/material';

const Footer = () => {
  return (
    <footer style={{ padding: '20px', backgroundColor: '#1976d2', color: '#fff', marginTop: '40px' }}>
      <Container>
        <Typography variant="body2" align="center">
          © {new Date().getFullYear()} Alzheimer Detection. All rights reserved.
        </Typography>
      </Container>
    </footer>
  );
};

export default Footer;