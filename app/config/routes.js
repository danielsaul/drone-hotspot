import React from 'react';
import { Scene, Router, Actions, ActionConst } from 'react-native-router-flux';
import Main from '../layouts/main';

const scenes = Actions.create(
  <Scene key="root">
    <Scene key="main" component={Main} title="Drone Hotspot" initial={true} />
  </Scene>
);

export default () => (
  <Router scenes={scenes} />
);
