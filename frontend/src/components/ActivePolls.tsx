import { Card, Grid, Typography } from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import React from "react";
import { useSummary } from "../api/useData";
import * as styles from '../styles/styles';
import { PollSummary } from './PollSummary';
import { SectionTitle } from "./SectionTitle";

export const ActivePolls = ({ viewMoreHandler }: { viewMoreHandler: Function }) => {

  const { polls, isValidating } = useSummary();

  const skeletons = (
    <Grid container item
      spacing={1}
      direction="column"
      justify="space-between"
      alignItems="center">
      {Array(3).fill(3).map(() => (
        <Grid item
          spacing={2}
          direction="row">
          <Skeleton variant="rect" width={800} height={100} />
        </Grid>
      ))}
    </Grid>
  );

  const haveData = !isValidating || polls
  const summary = polls.length ?
    polls.map((poll: any) => (<PollSummary {...poll} />))
    : <Grid item><Typography>There are no active polls right now.</Typography></Grid>

  return (
    <Card style={styles.mainCard}>
      <Grid container
        direction="row"
        justify="space-between"
        alignItems="center">
        <SectionTitle title="Active Polls" subtitle="Make sure to connect to the server to vote!" buttonText="View All" buttonAction={() => viewMoreHandler()} />
      </Grid>
      <Grid spacing={2} container>
        {haveData ? summary : skeletons}
      </Grid>
    </Card>
  );
}
