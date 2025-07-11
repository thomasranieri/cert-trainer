import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { QuizStats } from '../types';

interface ProgressBarProps {
  currentQuestion: number;
  totalQuestions: number;
  stats: QuizStats;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  currentQuestion,
  totalQuestions,
  stats
}) => {
  const progress = totalQuestions > 0 ? (currentQuestion / totalQuestions) * 100 : 0;

  return (
    <View style={styles.header}>
      <Text style={styles.questionCounter}>
        Question {currentQuestion} of {totalQuestions}
      </Text>
      <View style={styles.statsContainer}>
        <Text style={styles.stats}>
          Score: {stats.correct}/{stats.total} ({stats.percentage}%)
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  questionCounter: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  statsContainer: {
    backgroundColor: '#E3F2FD',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  stats: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1976D2',
  },
});
