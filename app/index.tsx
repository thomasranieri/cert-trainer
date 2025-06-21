import React from 'react';
import { StyleSheet, View } from 'react-native';
import MainApp from './components/MainApp';

export default function Index() {
  return (
    <View style={styles.container}>
      <MainApp />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
