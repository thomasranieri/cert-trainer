import { router } from 'expo-router';
import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

interface ExamCardProps {
  exam: {
    name: string;
    count: number;
  };
}

const ExamCard: React.FC<ExamCardProps> = ({ exam }) => {
  return (
    <TouchableOpacity
      style={styles.examCard}
      onPress={() => router.push(`/quiz?exam=${exam.name}&type=unseen`)}
    >
      <Text style={styles.examTitle}>{exam.name}</Text>
      <Text style={styles.examCount}>{exam.count} questions</Text>
      <View style={styles.startButton}>
        <Text style={styles.startButtonText}>Start Quiz</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  examCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    maxWidth: '100%',
    width: 300,
  },
  examTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  examCount: {
    fontSize: 14,
    color: '#666',
    marginBottom: 16,
  },
  startButton: {
    backgroundColor: '#2196F3',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  startButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default ExamCard;
