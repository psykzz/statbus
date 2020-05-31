import { Card, Grid, makeStyles, Typography } from "@material-ui/core";
import React from "react";
import { useSummary, useWinrates } from "../api/useData";

const useStyles = makeStyles({
  mainCard: {
    backgroundColor: '#4E5D6C',
    padding: '50px',
    marginTop: '25px'
  }
})

export const StatBanner = () => {
  const cx = useStyles();
  const { stats } = useSummary();
  const { winrates } = useWinrates();

  return (
    <Card className={cx.mainCard}>
      <Grid container
        justify="space-around"
        direction="row">
        <Grid item>
          <Typography variant="h2">Statbus</Typography>
          <Typography variant="h6"> Welcome to the TGMC Statbus!</Typography>
        </Grid>
        <Grid item>
          <Typography variant="h6">Tracking</Typography>
          <Typography> {stats.rounds} Rounds</Typography>
          <Typography> {stats.players} Players</Typography>
        </Grid>
        <Grid item>
          <Typography variant="h6">Current Winrates</Typography>
          <Grid container
            justify="space-between"
            direction="row">
            <Grid item >
              <Typography style={{ width: '75px', display: 'inline-block' }}>Marine</Typography>
              <Typography>{winrates["Marine Major Victory"]}</Typography>
              <Typography>{winrates["Marine Minor Victory"]}</Typography>
            </Grid>
            <Grid item>
              <Typography style={{ width: '75px', display: 'inline-block' }}>Xeno</Typography>
              <Typography>{winrates["Xenomorph Major Victory"]}</Typography>
              <Typography>{winrates["Xenomorph Minor Victory"]}</Typography>
            </Grid>
            <Grid item>
              <Typography>&nbsp;</Typography>
              <Typography> Major</Typography>
              <Typography> Minor</Typography>
            </Grid>
          </Grid>


        </Grid>
      </Grid>
    </Card >
  );
}
