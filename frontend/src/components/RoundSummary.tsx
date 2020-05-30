import { Grid, Link, Typography } from "@material-ui/core"
import React from "react"
import { useHistory } from "react-router-dom"
import { useRound } from "../api/useData";
import { Skeleton } from "@material-ui/lab";

export const RoundSummary = ({ roundId }: any) => {

  const { push } = useHistory();
  const { round:
    { id, game_mode, map_name, game_mode_result, ship_name, players, deaths } } = useRound(roundId);

  if (!id) {
    return <p><Skeleton variant="rect" width={1200} height={40} /></p>
  }
  return (<Grid container item
    justify="space-between"
    alignContent="center"
    alignItems="center" spacing={3}>
    <Grid item>
      <Typography variant="h5">
        <Link onClick={() => push(`/round/${id}`)}>
          #{id}
        </Link>
      </Typography>
    </Grid>
    <Grid item style={{ marginRight: 'auto' }}>
      <Typography>{game_mode} on {map_name} {ship_name}</Typography>
      <Typography>{game_mode_result}</Typography>
    </Grid>
    <Grid item>
      <Typography>{players?.length ?? 0} Players </Typography>
      <Typography>{deaths?.length ?? 0} deaths </Typography>
    </Grid>
  </Grid>);
}
