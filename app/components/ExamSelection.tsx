import AntDesign from '@expo/vector-icons/AntDesign';

import { Link, router } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  useWindowDimensions,
} from 'react-native';
import { Question } from '../../services/DatabaseService';
import questionsData from '../data/questions.json';

const ExamSelection: React.FC = () => {
  const [availableExams, setAvailableExams] = useState<{ name: string; count: number }[]>([]);
  const { width } = useWindowDimensions();
  const isNarrowScreen = width < 768; // Adjust this breakpoint as needed

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

      <ScrollView style={styles.scrollContainer} showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContentContainer}>
        <View style={styles.content}>
          <View style={styles.examGrid}>
            {availableExams.map(exam => renderExamCard(exam))}
          </View>
          <Text style={{ textAlign: 'center', marginTop: 20 }}>
            <p>This website is not affiliated with AWS or any other certification body.</p>
            <p>These questions are not official and are for study purposes only. Certification questions will differ.</p>
            <p>All trademarks and copyrights are the property of their respective owners.</p>
            <p>Made by <a href="https://thomasranieri.dev/">Thomas Ranieri</a> for my own study purposes.</p>
            <p>See <a href="https://github.com/thomasranieri/cert-trainer">GitHub</a> for more information and known limitations.</p>
          </Text>
        </View>
        <footer style={styles.getInTouch}>
          <Link href="https://www.linkedin.com/in/thomas-ranieri-dev/" style={styles.socialLink} target='_blank'>
            <AntDesign name="linkedin-square" size={24} color="white" />
            {!isNarrowScreen && <Text style={styles.getInTouchText}>thomas-ranieri-dev</Text>}
          </Link>
          <Link href="https://github.com/thomasranieri/cert-trainer" style={styles.socialLink} target='_blank'>
            <AntDesign name="github" size={24} color="white" />
            {!isNarrowScreen && <Text style={styles.getInTouchText}>thomasranieri/cert-trainer</Text>}
          </Link>
          <Link href="mailto:tom@classgen.com" style={styles.socialLink} target='_blank'>
            <AntDesign name="mail" size={24} color="white" />
            {!isNarrowScreen && <Text style={styles.getInTouchText}>tom@classgen.com</Text>}
          </Link>
        </footer>
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
  scrollContentContainer: {
    flexGrow: 1,
  },
  content: {
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
  getInTouch: {
    marginTop: 20,
    backgroundColor: '#5252bb',
    flexDirection: 'row',
    display: 'flex',
    justifyContent: 'space-around',
  },
  socialLink: {
    justifyContent: 'center',
    alignItems: 'center',
    display: 'flex',
    padding: 10,
  },
  getInTouchText: {
    color: 'white',
    fontSize: 16,
    marginLeft: 8,
  },
});

export default ExamSelection;
