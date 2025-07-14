import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  useWindowDimensions,
} from 'react-native';
import ExamCard from '../../components/ExamCard';
import SocialFooter from '../../components/SocialFooter';
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

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Select an Exam</Text>
        <Text style={styles.headerSubtitle}>Choose which certification you want to study for</Text>
      </View>

      <ScrollView style={styles.scrollContainer} showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContentContainer}>
        <View style={styles.content}>
          <View style={styles.examGrid}>
            {availableExams.map(exam => (
              <ExamCard key={exam.name} exam={exam} />
            ))}
          </View>
          <Text style={{ textAlign: 'center', marginTop: 20 }}>
            <p>This website is not affiliated with AWS or any other certification body.</p>
            <p>These questions are not official and are for study purposes only. Certification questions will differ.</p>
            <p>All trademarks and copyrights are the property of their respective owners.</p>
            <p>Made by <a href="https://thomasranieri.dev/" target="_blank">Thomas Ranieri</a> for my own study purposes.</p>
            <p>See <a href="https://github.com/thomasranieri/cert-trainer" target="_blank">GitHub</a> for more information and known limitations.</p>
          </Text>
        </View>
        <SocialFooter isNarrowScreen={isNarrowScreen} />
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
    display: 'flex',
    flexWrap: 'wrap',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'stretch',
  },
});

export default ExamSelection;
