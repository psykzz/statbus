import React from "react";
import { Paper, Card } from "@material-ui/core";
import { StatBanner, ActivePolls, RecentRounds } from "../components";
import { useHistory } from "react-router-dom";


export const Home = () => {
  const { push } = useHistory()

  const viewMorePollsHandler = React.useCallback(() => {
    push('/polls');
  }, [push]);

  const viewAllRoundsHandler = React.useCallback(() => {
    push('/rounds');
  }, [push]);

  return (
    <>
      <StatBanner />
      <ActivePolls viewMoreHandler={viewMorePollsHandler} />
      <RecentRounds viewMoreHandler={viewAllRoundsHandler} />
    </>
  );
}
