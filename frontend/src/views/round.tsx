import { Grid, Typography } from "@material-ui/core";
import React from "react";
import { useRound } from "../api/useData";
import { RoundDeaths } from "../components/RoundDeaths";
import { RoundStats } from "../components/RoundStats";
import { TestMergeSummary } from "../components/TestMergeSummary";
export const Round = ({ match }: any) => {
  const { params: { id } } = match;
  const { round } = useRound(id);
  return (
    <Grid container
      justify="space-between">
      <Grid container item justify="flex-end">
        <Grid item>
          <Typography variant="h3">Round #{round.id}</Typography>
        </Grid>
        <Grid item>
          <RoundDeaths roundId={id} />
        </Grid>
        <Grid item>
          <RoundStats roundId={id} />
        </Grid>
      </Grid>
      <Grid container item justify="space-between">
        <Grid item>
          <TestMergeSummary roundId={id} />
        </Grid>
      </Grid>
    </Grid>
  );
}
