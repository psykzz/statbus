import React from 'react';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { TitleBar } from './components/TitleBar';
import { AppRouter } from './routes';
import { Router, Route, Redirect } from 'react-router';
import { createBrowserHistory } from 'history';
import ReactGA from 'react-ga';
import './App.scss';
import { Container, Grid } from '@material-ui/core';
import { Footer } from './components';

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
      <Router history={customHistory}>
        <Grid
          container
          direction="row"
          justify="center"
          alignItems="center"
        >
          <TitleBar />
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
