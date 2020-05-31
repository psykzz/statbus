import { Container, Grid, CssBaseline } from '@material-ui/core';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createBrowserHistory } from 'history';
import React from 'react';
import ReactGA from 'react-ga';
import { Router } from 'react-router';
import './App.scss';
import { Footer } from './components';
import { TitleBar } from './components/TitleBar';
import { AppRouter } from './routes';


const customHistory = createBrowserHistory();

ReactGA.initialize('UA-153492320-1');
customHistory.listen(location => {
  ReactGA.set({ page: location.pathname }); // Update the user's current page
  ReactGA.pageview(location.pathname); // Record a pageview for the given page
});

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const theme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: prefersDarkMode ? 'dark' : 'light',
        },

      }),
    [prefersDarkMode],
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router history={customHistory}>
        <Grid
          container
          direction="row"
          justify="center"
          alignItems="center"
        >
          <Container>
            <AppRouter />
            <Footer />
          </Container>
        </Grid>
      </Router>
    </ThemeProvider>
  );
}

export default App;
