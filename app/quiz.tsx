import { useLocalSearchParams, useNavigation, useRouter } from 'expo-router';
import Head from 'expo-router/head';
import React from 'react';
import { SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import Quiz from './components/Quiz';

type Params = { exam?: string };

export default function QuizPage() {
  const router = useRouter();
  const { exam } = useLocalSearchParams<Params>();
  const navigation = useNavigation();

  return (
    <>
      <Head>
        <title>{exam ? `${exam} Quiz - Cert Trainer` : 'Quiz - Cert Trainer'}</title>
      </Head>
      <SafeAreaView style={styles.container}>
        <View style={styles.navbar}>
          <Text style={styles.appTitle}>{exam || 'Quiz'}</Text>
          <View style={styles.navButtons}>
            <TouchableOpacity
              style={[styles.navButton, styles.activeNavButton]}
              onPress={() => router.replace(`/quiz?exam=${exam}`)}
            >
              <Text style={[styles.navButtonText, styles.activeNavButtonText]}>
                Quiz
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.navButton}
              onPress={() => router.replace(`/stats?exam=${exam}`)}
            >
              <Text style={styles.navButtonText}>
                Stats
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Quiz Content */}
        <View style={styles.screenContainer}>
          <Quiz
            selectedExam={exam || ''}
            onBackToHome={() => router.push('/')}
          />
        </View>
      </SafeAreaView>
    </>
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
