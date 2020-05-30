import { Card, Grid, makeStyles, Typography } from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import React from "react";
import { useSummary } from "../api/useData";
import { RoundSummary } from './RoundSummary';
import { SectionTitle } from "./SectionTitle";


const useStyles = makeStyles({
  root: {},
  mainCard: {
    backgroundColor: '#4E5D6C',
    padding: '10px',
    marginTop: '25px',
    marginBottom: '25px'
  }
});

export const RecentRounds = ({ viewMoreHandler }: { viewMoreHandler: Function }) => {
  const cx = useStyles();
  const { rounds, isValidating } = useSummary();

  const skeletons = (
    <Grid container item
      spacing={1}
      direction="column"
      justify="space-between"
      alignItems="center">
      {Array(5).fill(5).map(() => (
        <Grid item
          direction="row"
          justify="space-between"
          alignItems="center">
          <Skeleton variant="rect" width={800} height={100} />
        </Grid>
      ))}
    </Grid>
  );

  const haveData = !isValidating || rounds
  const summary = rounds.length ?
    rounds.map((roundId: number) => (<RoundSummary roundId={roundId} />))
    : <Grid item><Typography>There hasn't been any recent rounds.</Typography></Grid>

  return (
    <Card className={cx.mainCard}>
      <Grid container
        direction="row"
        justify="space-between"
        alignItems="center">
        <SectionTitle title="Recent Rounds" subtitle="Only the last few rounds are shown" buttonText="View All" buttonAction={() => viewMoreHandler()} />
      </Grid>
      <Grid container spacing={2}>
        {haveData ? summary : skeletons}
      </Grid>
    </Card>
  );
}
