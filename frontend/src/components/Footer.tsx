import { Grid, makeStyles, Paper, Typography, List, ListItem, ListItemText, Box } from "@material-ui/core";
import React from "react";
import { Link } from "react-router-dom";

const useStyles = makeStyles({
  root: {
    height: '250px'
  },
  tgmcLogo: {
    display: 'block', height: '150px', width: '150px'
  }
});

export const Footer = () => {
  const cx = useStyles();

  return (
    <Paper className={cx.root}>
      <Grid
        container
        alignItems="center"
        justify="space-between"
        direction="column">
        <Grid container
          justify="space-around"
          direction="row">
          <Box>
            <Typography variant="h5">TerraGov Marine Corps</Typography>
            <img className={cx.tgmcLogo} src='https://tgstation13.org/wiki/images/thumb/9/96/TGMC_logo.png/160px-TGMC_logo.png' alt="tgmc logo" />
          </Box>
          <Box>
            <Typography variant="h5">Quick links</Typography>
            <List component="nav" aria-label="main mailbox folders">
              <ListItem button component="a" href="/play">
                <ListItemText primary="Play now" />
              </ListItem>
              <ListItem button component="a" href="/">
                <ListItemText primary="Home" />
              </ListItem>
              <ListItem button component="a" href="/discord">
                <ListItemText primary="Discord" />
              </ListItem>
              <ListItem button component="a" href="/wiki">
                <ListItemText primary="Get Started" />
              </ListItem>
            </List>
          </Box>
        </Grid>
        <Box m={3}><Typography><Link to='/github'>TerraGov Marine Corps</Link> is a terrible game.</Typography></Box>
      </Grid>
    </Paper>
  );
}
