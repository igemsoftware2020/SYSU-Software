import { Button, Card, Classes, Elevation, H1, H2, H5, Menu, MenuItem, Popover } from "@blueprintjs/core";
import * as React from "react";
import { Container, Row, Col } from "react-grid-system";
import { IconNames } from "@blueprintjs/icons";

const CreateMenu: React.FunctionComponent = () => (
  <Menu>
    <MenuItem text="Manually" icon={IconNames.DOCUMENT} href="/designer" />
    <MenuItem text="Image Recognition" icon={IconNames.MEDIA} href="/designer#image" />
    <MenuItem text="Genenet-guided" icon={IconNames.EXCHANGE} href="/designer#genenet" />
  </Menu>
);

export const Home: React.FunctionComponent = () => {
  return (
    <Container>
      <H1 className="igem-mt-medium">Maloadis</H1>

      <H2>
        <span className="igem-pr-medium">
          <b>Dashboard</b>
        </span>
        <span className="igem-pr-medium">Explore</span>
      </H2>
      <Popover content={<CreateMenu />} position="bottom">
        <Button
          rightIcon={IconNames.CARET_DOWN}
          icon={IconNames.ADD}
          text="New Design"
          minimal
          className="igem-mt-small igem-mb-small"
        />
      </Popover>
      <Row>
        <Col xs={3}>
          <Card interactive={true} elevation={Elevation.TWO}>
            <H5>
              <a href="#">Sample design 1</a>
            </H5>
            <p>Card content</p>
          </Card>
        </Col>
        <Col xs={3}>
          <Card interactive={true} elevation={Elevation.TWO}>
            <H5>
              <a href="#">Sample design 2</a>
            </H5>
            <p>Card content</p>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};
