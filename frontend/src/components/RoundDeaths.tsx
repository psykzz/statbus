import { Card, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@material-ui/core";
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
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell align="right">Araea</TableCell>
              <TableCell align="right">Time of Death</TableCell>
              <TableCell align="right">Health</TableCell>
              <TableCell align="right">Coords</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {deaths.map((row: any) => (
              <TableRow key={row.name}>
                <TableCell component="th" scope="row">
                  {row.name}
                </TableCell>
                <TableCell align="right">{row.pod}</TableCell>
                <TableCell align="right">{row.tod}</TableCell>
                <TableCell align="right">
                  <div>{row.bruteloss}</div>
                  <div>{row.fireloss}</div>
                  <div>{row.toxloss}</div>
                  <div>{row.oxyloss}</div>
                  {/* <div>{row.brainloss}</div>
                  <div>{row.cloneloss}</div>
                  <div>{row.staminaloss}</div> */}
                </TableCell>
                <TableCell align="right">{row.x_coord}, {row.y_coord}, {row.z_coord}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Card>
  )
}
