import { useRouter } from 'expo-router';
import React from 'react';
import { StyleSheet, View } from 'react-native';
import ExamSelection from './components/ExamSelection';

export default function Index() {
  const router = useRouter();
  return (
    <View style={styles.container}>
      <ExamSelection  />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
