import { Grid, Link, makeStyles, Typography } from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import React from "react";
import { useHistory } from "react-router-dom";
import { usePoll } from "../api/useData";

const useStyles = makeStyles({
  pushLeft: {
    marginRight: 'auto'
  },
  link: {
    width: '50px'
  },
  status: {
    width: '160px', padding: '10px',
  }
});

export const PollSummary = ({ pollId }: any) => {
  const cx = useStyles();
  const { push } = useHistory();

  const { poll:
    { id, createdby_ckey, question, starttime } } = usePoll(pollId);

  if (!id) {
    return <p><Skeleton variant="rect" width={1200} height={40} /></p>
  }

  return <Grid container item
    wrap='nowrap'
    justify="space-between"
    alignContent="center"
    alignItems="center">
    <Grid item>
      <Typography variant="h5" className={cx.link}>
      #{id}
      </Typography>
    </Grid>
    <Grid item className={cx.pushLeft}>
      <Typography variant="subtitle2" >{createdby_ckey} asks...</Typography>
      <Typography>{question}</Typography>
    </Grid>
    <Grid item>
      <Typography className={cx.status}>Login to vote</Typography>
    </Grid>
  </Grid>;
}
