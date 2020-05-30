import { Grid, makeStyles, Paper, Typography } from "@material-ui/core";
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
          <div>
            <Typography variant="h5">TerraGov Marine Corps</Typography>
            <img className={cx.tgmcLogo} src='https://tgstation13.org/wiki/images/thumb/9/96/TGMC_logo.png/160px-TGMC_logo.png' alt="tgmc logo" />
          </div>
          <div >
            <Typography variant="h5">Quick links</Typography>
            <ul>
              <li><Link to='/play'>Play now</Link></li>
              <li><Link to='/'>Homepage</Link></li>
              <li><Link to='/discord'>Discord</Link></li>
              <li><Link to='/wiki'>Get Started</Link></li>
            </ul>
          </div>
        </Grid>
        <div><Link to='/github'>TerraGov Marine Corps</Link> is a terrible game.</div>
      </Grid>
    </Paper>
  );
}
