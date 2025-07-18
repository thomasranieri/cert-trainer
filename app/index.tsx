import Head from 'expo-router/head';
import React from 'react';
import { StyleSheet, View } from 'react-native';
import ExamSelection from './components/ExamSelection';

export default function Index() {
  return (
    <>
      <Head>
        <title>Cert Trainer</title>
      </Head>
      <View style={styles.container}>
        <ExamSelection />
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
