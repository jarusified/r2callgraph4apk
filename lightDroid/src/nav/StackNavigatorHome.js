import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';

import Home from '../screens/home/Home';
import Summary from "../screens/summary/Summary";

const Stack = createStackNavigator();

export default function StackNavigatorHome() {
  return (
    <Stack.Navigator initialRouteName="Home" mode="modal">
      <Stack.Screen
        name="Home"
        component={Home}
        options={{
          headerTitleAlign: 'center',
        }}
      />
      <Stack.Screen
        name="Summary"
        component={Summary}
        options={{
          headerTitleAlign: 'center',
        }}
      />
    </Stack.Navigator>
  );
}
