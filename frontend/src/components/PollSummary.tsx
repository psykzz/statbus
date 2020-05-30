import { Grid, Link, makeStyles, Typography } from "@material-ui/core";
import React from "react";
import { useHistory } from "react-router-dom";

const useStyles = makeStyles({
  pushLeft: {
    marginRight: 'auto'
  },
  roundLink: {
    width: '50px'
  },
  status: {
    width: '160px', padding: '10px'
  }
});

export const PollSummary = ({ id, author, question, status_text }: any) => {
  const cx = useStyles();
  const { push } = useHistory();

  return <Grid container item
    wrap='nowrap'
    justify="space-between"
    alignContent="center"
    alignItems="center">
    <Grid item>
      <Typography variant="h5" className={cx.roundLink}>
        <Link onClick={() => push(`/poll/${id}`)}>
          #{id}
        </Link>
      </Typography>
    </Grid>
    <Grid item className={cx.pushLeft}>
      <Typography variant="subtitle2" >{author} asks...</Typography>
      <Typography>{question}</Typography>
    </Grid>
    <Grid item>
      <Typography className={cx.status}>{status_text}</Typography>
    </Grid>
  </Grid>;
}
