import React from 'react';
import {View, Text, StyleSheet} from 'react-native';

const styles = StyleSheet.create({
  body: {
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default function Home() {
  return (
    <View style={styles.body}>
      <Text>TODO: Work here</Text>
    </View>
  );
}
