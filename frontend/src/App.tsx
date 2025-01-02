import React, { useEffect, useState } from 'react';
import { 
  Container, 
  Typography, 
  Paper, 
  Grid,
  Card,
  CardContent,
  Box
} from '@mui/material';
import axios from 'axios';

interface User {
  username: string;
  btc_amount: number;
  usd_value: number;
  is_admin: boolean;
}

interface WalletInfo {
  total_btc: number;
  btc_price: number;
  total_usd_value: number;
}

function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [walletInfo, setWalletInfo] = useState<WalletInfo | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [usersResponse, walletResponse] = await Promise.all([
          axios.get('http://localhost:5000/api/users'),
          axios.get('http://localhost:5000/api/wallet-info')
        ]);
        setUsers(usersResponse.data);
        setWalletInfo(walletResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Aggiorna ogni 30 secondi
    return () => clearInterval(interval);
  }, []);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        Bitcoin Wallet Condiviso
      </Typography>

      {walletInfo && (
        <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box textAlign="center">
                <Typography variant="h6" color="text.secondary">
                  Bitcoin Totali
                </Typography>
                <Typography variant="h4">
                  {walletInfo.total_btc.toFixed(4)} BTC
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box textAlign="center">
                <Typography variant="h6" color="text.secondary">
                  Prezzo Bitcoin
                </Typography>
                <Typography variant="h4">
                  ${walletInfo.btc_price.toLocaleString()}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box textAlign="center">
                <Typography variant="h6" color="text.secondary">
                  Valore Totale
                </Typography>
                <Typography variant="h4">
                  ${walletInfo.total_usd_value.toLocaleString()}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      )}

      <Grid container spacing={3}>
        {users.map((user) => (
          <Grid item xs={12} sm={6} md={4} key={user.username}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  {user.username}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Bitcoin: {user.btc_amount.toFixed(4)} BTC
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Valore: ${user.usd_value.toLocaleString()}
                </Typography>
                {user.is_admin && (
                  <Typography variant="body2" color="primary">
                    Admin
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default App; 