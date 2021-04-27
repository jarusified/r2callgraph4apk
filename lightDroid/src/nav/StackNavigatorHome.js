import React from 'react';
import {useIsFocused} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';

import Home from '../screens/home/Home';

const Stack = createStackNavigator();

export default function StackNavigatorHome() {
  const isFocusedRef = React.useRef(true);
  isFocusedRef.current = useIsFocused();

  return (
    <Stack.Navigator initialRouteName="Home" mode="modal">
      <Stack.Screen
        name="Home"
        component={Home}
        options={{
          headerTitleAlign: 'center',
        }}
      />
    </Stack.Navigator>
  );
}
