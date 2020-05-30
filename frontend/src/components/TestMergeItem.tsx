import { ListItem, ListItemText } from "@material-ui/core";
import React from "react";

export const TestMergeItem = ({ number, title, user: { login: author = "" } = {} }: any) => {
  const onClickHandler = () => window.location.href = `https://github.com/tgstation/TerraGov-Marine-Corps/pull/${number}`
  return (
    <ListItem button onClick={onClickHandler}>
      <ListItemText primary={`#${number} ${title} by ${author}`} />
    </ListItem>
  )
}
