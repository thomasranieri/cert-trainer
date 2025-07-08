import { useRouter, useSearchParams } from 'expo-router';
import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

const MainApp: React.FC = () => {
  const router = useRouter();
  const { exam } = useSearchParams<{ exam?: string }>();
  const selectedExam = exam ?? '';

  const handleExamSelect = (examName: string) => {
    router.push({ pathname: '/quiz', params: { exam: examName } });
  };

  const handleBackToHome = () => router.push('/');

  return (
    <SafeAreaView style={styles.container}>
      {/* Navigation Header */}
      <View style={styles.navbar}>
        <Text style={styles.appTitle}>{selectedExam || 'Cert Trainer'}</Text>
        { /* Only show tabs on quiz or stats pages */ }
        {selectedExam !== '' && (
          <View style={styles.navButtons}>
            <TouchableOpacity
              style={[
                styles.navButton,
                router.pathname.startsWith('/quiz') && styles.activeNavButton,
              ]}
              onPress={() => router.push('/quiz?exam=' + selectedExam)}
            >
              <Text
                style={[
                  styles.navButtonText,
                  router.pathname.startsWith('/quiz') && styles.activeNavButtonText,
                ]}
              >
                Quiz
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.navButton,
                router.pathname.startsWith('/stats') && styles.activeNavButton,
              ]}
              onPress={() => router.push('/stats?exam=' + selectedExam)}
            >
              <Text
                style={[
                  styles.navButtonText,
                  router.pathname.startsWith('/stats') && styles.activeNavButtonText,
                ]}
              >
                Stats
              </Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      {/* Screen Content */}
      <View style={styles.screenContainer}>
        {/* Nested routes will render here via router outlet */}
        {/* In expo-router, pages are separate files; this component remains layout header only */}
      </View>
    </SafeAreaView>
  );
};

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

export default MainApp;
