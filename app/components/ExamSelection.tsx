import { router } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { Question } from '../../services/DatabaseService';
import questionsData from '../data/questions.json';

const ExamSelection: React.FC = () => {
  const [availableExams, setAvailableExams] = useState<{ name: string; count: number }[]>([]);

  useEffect(() => {
    // Extract unique exams from questions data
    const questions = questionsData as Question[];
    const examCounts: { [key: string]: number } = {};
    
    questions.forEach(question => {
      if (question.exam) {
        examCounts[question.exam] = (examCounts[question.exam] || 0) + 1;
      }
    });

    const exams = Object.entries(examCounts).map(([name, count]) => ({
      name,
      count,
    })).sort((a, b) => a.name.localeCompare(b.name));

    setAvailableExams(exams);
  }, []);

  const renderExamCard = (exam: { name: string; count: number }) => (
    <TouchableOpacity
      key={exam.name}
      style={styles.examCard}
      onPress={() => router.push(`/quiz?exam=${exam.name}`)}
    >
      <Text style={styles.examTitle}>{exam.name}</Text>
      <Text style={styles.examCount}>{exam.count} questions</Text>
      <View style={styles.startButton}>
        <Text style={styles.startButtonText}>Start Quiz</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Select an Exam</Text>
        <Text style={styles.headerSubtitle}>Choose which certification you want to study for</Text>
      </View>
      
      <ScrollView style={styles.scrollContainer} showsVerticalScrollIndicator={false}>
        <View style={styles.examGrid}>
          {availableExams.map(exam => renderExamCard(exam))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: 'white',
    paddingHorizontal: 20,
    paddingVertical: 24,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  scrollContainer: {
    flex: 1,
  },
  examGrid: {
    padding: 20,
    gap: 16,
  },
  examCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
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

export default ExamSelection;
