import React from "react";
import { useHistory } from "react-router-dom";
import { ActivePolls, RecentRounds, StatBanner } from "../components";


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
