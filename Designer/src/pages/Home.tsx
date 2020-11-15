import { Alignment, Button, Card, Classes, Elevation, H1, H2, H5, Menu, MenuItem, Popover } from "@blueprintjs/core";
import * as React from "react";
import { Container, Row, Col } from "react-grid-system";
import { IconNames } from "@blueprintjs/icons";
import { Link } from "react-router-dom";

export const Home: React.FunctionComponent = () => {
  return (
    <Container>
      <Row className="igem-mt-medium">
        <Col>
          <img src={require("url:../assets/main_logo.jpg")} height="180px" />
        </Col>
        <Col />
        <Col />
      </Row>
      <Row className="igem-mt-medium">
        <Col />
        <Col>
          <img useMap="#guidemap" src={require("url:../assets/guide.jpg")} height="250px" />
          <map name="guidemap" id="guidemap">
            <area shape="circle" coords="320,50,40" href="/designer#search" alt="Search" />
            <area shape="circle" coords="320,200,40" href="/designer" alt="Design" />
            <area shape="circle" coords="480,125,50" href="/designer#simulation" alt="Simulation" />
            <area shape="circle" coords="630,125,60" href="/designer#bayes" alt="Bayes" />
          </map>
        </Col>
        <Col />
      </Row>
      <Row className="igem-mt-medium">
        <Col />
        <Col>
          <Link to="/designer">
            <img src={require("url:../assets/logo.png")} height="100px" />
          </Link>
        </Col>
        <Col />
      </Row>
    </Container>
  );
};
