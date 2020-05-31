import React from "react";
import { Typography, Chip, Button, Box, Grid } from "@material-ui/core";

export const SectionTitle = ({ title, subtitle, buttonText, buttonAction }: any) => (
  <Grid container direction="row" justify="space-between">
    <Box m={3} marginTop={1}>
      <Typography component="span" variant="h3">{title}</Typography>
    </Box>
    <Chip variant="outlined" label={subtitle} />
    {/* <Button component="span" onClick={buttonAction}>{buttonText}</Button> */}
  </Grid>
)
