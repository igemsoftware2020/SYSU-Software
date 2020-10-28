import { Button, Card, Classes, Elevation, H1, H2, H5, Menu, MenuItem, Popover } from "@blueprintjs/core";
import * as React from "react";
import { Container, Row, Col } from "react-grid-system";
import { IconNames } from "@blueprintjs/icons";
import { Link } from "react-router-dom";

export const Home: React.FunctionComponent = () => {
  return (
    <Container>
      <img src={require("url:../assets/logo.png")} height="180px" />
      <H2 className="igem-mt-medium">
        <b>Create Design</b>
      </H2>
      <Row className="igem-mt-medium">
        <Col xs={3}>
          <Link to="/designer">
            <Card interactive={true} elevation={Elevation.TWO}>
              <H5>Manually</H5>
              <p>The tranditional way of designing, by manually crafting parts.</p>
            </Card>
          </Link>
        </Col>
        <Col xs={3}>
          <Link to="/designer#image">
            <Card interactive={true} elevation={Elevation.TWO}>
              <H5>Image Recognition</H5>
              <p>Import any design images, and recognize structured information.</p>
            </Card>
          </Link>
        </Col>
        <Col xs={3}>
          <Link to="/designer#genenet">
            <Card interactive={true} elevation={Elevation.TWO}>
              <H5>Genenet Guided</H5>
              <p>Use function to descibe target, and let Maloadis automatically infer design with Genenet.</p>
            </Card>
          </Link>
        </Col>
      </Row>
    </Container>
  );
};
