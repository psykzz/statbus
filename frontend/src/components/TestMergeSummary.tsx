import { List, Typography, Grid, Paper } from "@material-ui/core";
import React from "react";
import { usePullRequest, useRound } from "../api/useData";
import { TestMergeItem } from "./TestMergeItem";

export const TestMergeSummary = ({ roundId, filterByLabels = [] }: any) => {
  const { round: { testmerged_prs = {} }, isValidating: isValidatingRound } = useRound(roundId);
  const { data, isValidating: isValidatingPRData } = usePullRequest();

  const isValidating = isValidatingRound || isValidatingPRData;

  const filteredPullRequests = React.useMemo(() => {
    if (!data || !testmerged_prs) {
      return;
    }
    const pullRequestData: any = {}
    Object.values(data).forEach((pr: any) => pullRequestData[pr.number] = pr);
    // This can be used to grab any missing PR data
    // const hasIds = Object.keys(data);
    // const allPRNumbers = Object.keys(testmerged_prs);
    // const missingPrs = allPRNumbers.filter(pr => hasIds.indexOf(pr) === -1);
    return Object.keys(testmerged_prs).map(id => pullRequestData[id])
  }, [isValidating]);

  return (
    <Paper>
      <Typography variant="h6">Merged PRs</Typography>

      <List dense>
        {filteredPullRequests?.map((tm: any) => (<TestMergeItem {...tm} />))}
      </List>
    </Paper>
  )
}
