import React, { useState } from 'react';
import {
    SafeAreaView,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
} from 'react-native';
import Quiz from './Quiz';
import Stats from './Stats';

type Screen = 'quiz' | 'stats';

const MainApp: React.FC = () => {
  const [currentScreen, setCurrentScreen] = useState<Screen>('quiz');

  const renderScreen = () => {
    switch (currentScreen) {
      case 'quiz':
        return <Quiz />;
      case 'stats':
        return <Stats />;
      default:
        return <Quiz />;
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Navigation Header */}
      <View style={styles.navbar}>
        <Text style={styles.appTitle}>AWS MLA-C01 Quiz</Text>
        <View style={styles.navButtons}>
          <TouchableOpacity
            style={[
              styles.navButton,
              currentScreen === 'quiz' && styles.activeNavButton,
            ]}
            onPress={() => setCurrentScreen('quiz')}
          >
            <Text
              style={[
                styles.navButtonText,
                currentScreen === 'quiz' && styles.activeNavButtonText,
              ]}
            >
              Quiz
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.navButton,
              currentScreen === 'stats' && styles.activeNavButton,
            ]}
            onPress={() => setCurrentScreen('stats')}
          >
            <Text
              style={[
                styles.navButtonText,
                currentScreen === 'stats' && styles.activeNavButtonText,
              ]}
            >
              Stats
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Screen Content */}
      <View style={styles.screenContainer}>
        {renderScreen()}
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
    paddingHorizontal: 20,
    paddingVertical: 16,
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
