import React, { Component } from 'react';
import {
  Header,
  Container,
  Content,
  Icon,
  Text,
  Button,
  Segment
} from 'native-base';
import { View } from 'react-native';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux';
import MainHeader from '../../components/MainHeader'
import { MapView } from 'expo';

import styles from './styles';

const mapStateToProps = ({ location }) => ({ location });
const mapDispatchToProps = {};

class Main extends Component{
  constructor(){
    super();
    this.state = {}
  }

  componentWillReceiveProps(props) {
    if (!('map_region' in this.state)){
      map_region = {
        latitude: props.location.latitude,
        longitude: props.location.longitude,
        latitudeDelta: 0.001,
        longitudeDelta: 0.001,
      };
      this.setState({map_region});
    }
  }

  render(){
    return (
      <Container>
        <MainHeader />
        <Content>
          <View style={{flex: 1}}>
            <MapView region={this.state.map_region} showsUserLocation={true} style={{ alignSelf: 'stretch', height: 300 }} />
          </View>
          <View style={{flex: 1}}>
            <Text style={styles.centered}>
            <Text style={styles.label}>Your Location:</Text> {this.props.location.latitude.toFixed(5)}, {this.props.location.longitude.toFixed(5)}
            </Text>
          </View>

          <View style={styles.connectionstatus_view}>
            <Text style={styles.connectionstatus_txt}><Icon name='ios-plane' style={{fontSize: 15}} /> Drone Connected </Text>
          </View>

          <Segment>
          <Button first active>
            <Text>Fly to Point</Text>
          </Button>
          <Button last>
            <Text>Autonomous</Text>
          </Button>
          </Segment>

        </Content>
      </Container>
    );
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
