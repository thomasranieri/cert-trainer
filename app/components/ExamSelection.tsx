import React, { useMemo } from 'react';
import {
    SafeAreaView,
    ScrollView,
    StyleSheet,
    Text,
    View,
} from 'react-native';
import { useQuestions } from '../context/QuestionsContext';
import { useClientDimensions } from '../hooks/useClientDimensions';
import ExamCard from './ExamCard';
import SocialFooter from './SocialFooter';

const ExamSelection: React.FC = () => {
  const { width, isHydrated } = useClientDimensions();
  const { questions, loading, error, requestedUrl, source } = useQuestions();
  
  // Only use screen width after hydration to avoid mismatch
  const isNarrowScreen = isHydrated && width !== null ? width < 768 : false;

  const availableExams = useMemo(() => {
    const examCounts: Record<string, number> = {};

    questions.forEach(question => {
      if (question.exam) {
        examCounts[question.exam] = (examCounts[question.exam] || 0) + 1;
      }
    });

    return Object.entries(examCounts)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [questions]);

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading question set...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Select an Exam</Text>
        <Text style={styles.headerSubtitle}>Choose which certification you want to study for</Text>
        {requestedUrl && (
          <Text style={styles.datasetNotice} numberOfLines={2}>
            Question set: {requestedUrl}
          </Text>
        )}
        {source === 'local' && requestedUrl && error && (
          <View style={styles.noticeContainer}>
            <Text style={styles.noticeText}>
              Using bundled questions. Remote load failed: {error}
            </Text>
          </View>
        )}
      </View>

      <ScrollView style={styles.scrollContainer} showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContentContainer}>
        <View style={styles.content}>
          <View style={styles.examGrid}>
            {availableExams.map(exam => (
              <ExamCard key={exam.name} exam={exam} questionsUrl={requestedUrl}
              />
            ))}
            {availableExams.length === 0 && (
              <View style={styles.noticeContainer}>
                <Text style={styles.noticeText}>
                  No exams were found in this question set.
                </Text>
              </View>
            )}
          </View>
          <View style={styles.disclaimerContainer}>
            <Text style={styles.disclaimerText}>
              This website is not affiliated with AWS or any other certification body.
            </Text>
            <Text style={styles.disclaimerText}>
              These questions are not official and are for study purposes only. Certification questions will differ.
            </Text>
            <Text style={styles.disclaimerText}>
              All trademarks and copyrights are the property of their respective owners.
            </Text>
            <Text style={styles.disclaimerText}>
              Made by Thomas Ranieri for my own study purposes.
            </Text>
            <Text style={styles.disclaimerText}>
              See GitHub for more information and known limitations.
            </Text>
          </View>
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
  datasetNotice: {
    fontSize: 12,
    color: '#555',
    marginTop: 8,
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
  noticeContainer: {
    backgroundColor: '#FFF8E1',
    borderRadius: 12,
    padding: 16,
    marginTop: 16,
    marginHorizontal: 20,
  },
  noticeText: {
    color: '#8D6E63',
    fontSize: 14,
    textAlign: 'center',
  },
  disclaimerContainer: {
    marginTop: 20,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  disclaimerText: {
    textAlign: 'center',
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    lineHeight: 20,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
  },
});

export default ExamSelection;
