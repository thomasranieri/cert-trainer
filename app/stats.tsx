import { useLocalSearchParams, useRouter } from 'expo-router';
import React from 'react';
import { SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import Stats from './components/Stats';

type Params = { exam?: string };

export default function StatsPage() {
  const { exam } = useLocalSearchParams<Params>();
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      {/* Navigation Header */}
      <View style={styles.navbar}>
        <Text style={styles.appTitle}>{exam || 'Stats'}</Text>
        <View style={styles.navButtons}>
          <TouchableOpacity
            style={styles.navButton}
            onPress={() => router.push(`/quiz?exam=${exam}`)}
          >
            <Text style={styles.navButtonText}>
              Quiz
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.navButton, styles.activeNavButton]}
            onPress={() => router.push(`/stats?exam=${exam}`)}
          >
            <Text style={[styles.navButtonText, styles.activeNavButtonText]}>
              Stats
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Stats Content */}
      <View style={styles.screenContainer}>
        <Stats selectedExam={exam || ''} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  navbar: {
    backgroundColor: 'white',
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  appTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    flexShrink: 1,
    marginRight: 8,
    textAlign: 'left',
  },
  navButtons: {
    flexDirection: 'row',
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    padding: 4,
  },
  navButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 6,
  },
  activeNavButton: {
    backgroundColor: '#2196F3',
  },
  navButtonText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#666',
  },
  activeNavButtonText: {
    color: 'white',
  },
  screenContainer: {
    flex: 1,
  },
});
