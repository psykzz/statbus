import { Card, Grid, makeStyles, Typography } from "@material-ui/core";
import React from "react";
import { useSummary } from "../api/useData";

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

  return (
    <Card className={cx.mainCard}>
      <Grid container
        justify="space-around"
        direction="row">
        <Grid>
          <Typography variant="h2">Statbus</Typography>
          <Typography variant="h6"> Welcome to the TGMC Statbus!</Typography>
        </Grid>
        <Grid>
          <Typography variant="h6"> Tracking</Typography>
          <Typography> {stats.rounds} Rounds</Typography>
          <Typography> {stats.players} Players</Typography>
        </Grid>
      </Grid>
    </Card>
  );
}
