import { Grid, Typography, Paper, Box } from "@material-ui/core";
import React from "react";
import { useRound } from "../api/useData";
import { RoundDeaths } from "../components/RoundDeaths";
import { RoundStats } from "../components/RoundStats";
import { TestMergeSummary } from "../components/TestMergeSummary";
export const Round = ({ match }: any) => {
  const { params: { id } } = match;
  const { round } = useRound(id);
  return (
    <Box p={2}>
      <Grid container
        direction="column"
        justify="space-between">
        <Grid item>
          <Typography variant="h3">Round #{round.id}</Typography>
        </Grid>
        <Grid item>
          <RoundDeaths roundId={id} />
        </Grid>
        <Grid container direction="row" justify="space-between">
          <Grid item style={{ width: '45%' }}>
            <RoundStats roundId={id} />
          </Grid>
          <Grid item style={{ width: '45%' }}>
            <TestMergeSummary roundId={id} />
          </Grid>
        </Grid>
      </Grid>
    </Box>

  );
}
