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
      <Row className="igem-mt-medium">
        <H2 className="igem-mt-medium">
          <b>Fetured work</b>
        </H2>
      </Row>
      <Row className="igem-mt-medium">
        <Col xs={3}>
          <Link to="/designer#genenet">
            <Card style={{height: '150px'}} interactive={true} elevation={Elevation.TWO}>
              <H5>Automated Design</H5>
              <p>Automatically work out possible genetic circuits according to user's target gene expression demand.</p>
            </Card>
          </Link>
        </Col>
        <Col xs={3}>
          <Link to="/designer#image">
            <Card style={{height: '150px'}} interactive={true} elevation={Elevation.TWO}>
              <H5>Image Search</H5>
              <p>Search images by extracting part's and structural information from genetic circuit images.</p>
            </Card>
          </Link>
        </Col>
        <Col xs={3}>
          <Link to="/designer#bayes">
            <Card style={{height: '150px'}} interactive={true} elevation={Elevation.TWO}>
              <H5>Parameter Optimization</H5>
              <p>Improve wet-lab results by providing suggestions on parameter optimization.</p>
            </Card>
          </Link>
        </Col>
        <Col xs={3}>
          <Link to="/designer#simulation">
            <Card style={{height: '150px'}} interactive={true} elevation={Elevation.TWO}>
              <H5>Simulation</H5>
              <p>Simulate genetic circuit expression.</p>
            </Card>
          </Link>
        </Col>
      </Row>
      <Row style={{height: '50px'}} />
    </Container>
  );
};
