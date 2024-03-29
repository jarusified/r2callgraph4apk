import React, {useEffect} from 'react';
import {StyleSheet, View, ActivityIndicator} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';

import LocalStorage from 'lib/storages/LocalStorage';
import StackNavigatorHome from './src/nav/StackNavigatorHome';

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
  },
});

function App() {
  // For determining screen transition
  const routeNameRef = React.useRef();
  const navigationRef = React.useRef(null);
  const isFirstAppLaunch = React.useRef(false);

  const [
    isFirstAppLaunchResolved,
    setIsFirstAppLaunchResolved,
  ] = React.useState(false);

  useEffect(() => {
    LocalStorage.isFirstAppLaunch()
      .then(isFirst => {
        if (isFirst) {
          isFirstAppLaunch.current = true;
          LocalStorage.unsetFirstAppLaunch();
        }
        setIsFirstAppLaunchResolved(true);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  // Callback that's triggered when there's a screen transition
  const onStateChange = () => {
    const previousRouteName = routeNameRef.current;
    console.log('Previous state was: ', previousRouteName);

    const currentRoute = navigationRef.current.getCurrentRoute();
    if (!currentRoute) {
      return;
    }

    const currentRouteName = currentRoute.name;

    // Save the current route name for later comparision
    routeNameRef.current = currentRouteName;
  };

  function pickScreen() {
    if (!isFirstAppLaunchResolved) {
      return 'LOADING_SCREEN';
    }
    return 'HOME_SCREEN';
  }

  return (
    <NavigationContainer ref={navigationRef} onStateChange={onStateChange}>
      {(() => {
        switch (pickScreen()) {
          case 'HOME_SCREEN':
            return <StackNavigatorHome />;
          case 'LOADING_SCREEN':
          default:
            return (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#000" />
              </View>
            );
        }
      })()}
    </NavigationContainer>
  );
}

export default App;
