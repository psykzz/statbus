import { List, ListItem, Paper, Typography } from "@material-ui/core";
import React from "react";
import { useRound } from "../api/useData";

export const RoundStats = ({ roundId }: any) => {
  const { round: { round_stats = {} }, isValidating } = useRound(roundId);

  if (isValidating) {
    return null;
  }

  return (
    <Paper>
      <Typography variant="h6">Round stats</Typography>
      <List dense>
        {Object.keys(round_stats).map(stat => <ListItem>{`${stat.replace('_', ' ')} : ${round_stats[stat]}`}</ListItem>)}
      </List>
    </Paper>
  )
}
