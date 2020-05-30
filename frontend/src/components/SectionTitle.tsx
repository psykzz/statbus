import React from "react";
import { Typography, Chip, Button } from "@material-ui/core";

export const SectionTitle = ({ title, subtitle, buttonText, buttonAction }: any) => (
  <>
    <Typography component="span" variant="h3">{title}</Typography>
    <Chip variant="outlined" label={subtitle} />
    <Button component="span" onClick={buttonAction}>{buttonText}</Button>
  </>
)
