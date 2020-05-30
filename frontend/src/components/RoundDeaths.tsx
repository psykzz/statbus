import { Card, List, ListItem, Typography } from "@material-ui/core";
import React from "react";
import { useRound } from "../api/useData";
import * as styles from '../styles/styles';
export const RoundDeaths = ({ roundId }: any) => {
  const { round: { deaths = [] }, isValidating } = useRound(roundId);

  if (isValidating) {
    return null;
  }

  return (
    <Card style={styles.mainCard}>
      <Typography variant="h6">Deaths</Typography>
      <List dense>
        {deaths.map((death: any) => <ListItem>{`${death.name}`}</ListItem>)}
      </List>
    </Card>
  )
}
