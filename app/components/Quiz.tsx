import { useLocalSearchParams } from 'expo-router';
import React, { useMemo, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { ProgressBar } from '../../components/ProgressBar';
import { QuestionCard } from '../../components/QuestionCard';
import { QuizResults } from '../../components/QuizResults';
import { useQuiz } from '../../hooks/useQuiz';
import { Question } from '../../types';
import questionsData from '../data/questions.json';
import QuizFilters from './QuizFilters';

interface QuizProps {
  selectedExam: string;
  initialFilters?: {
    taskStatement: string | null;
    difficulty: string | null;
    type: 'all' | 'unseen';
  };
  onBackToHome: () => void;
}

type Params = { 
  exam?: string;
  task?: string;
  difficulty?: string;
  type?: 'all' | 'unseen';
};

const Quiz: React.FC<QuizProps> = ({ selectedExam, onBackToHome }) => {
  const routerParams = useLocalSearchParams<Params>();
  const insets = useSafeAreaInsets();
  const [allQuestions] = useState<Question[]>(questionsData as Question[]);
  const [showFilters, setShowFilters] = useState(false);

  // Memoize the options to prevent unnecessary re-renders
  const quizOptions = useMemo(() => ({
    selectedExam,
    task: routerParams.task,
    difficulty: routerParams.difficulty,
    type: routerParams.type,
  }), [selectedExam, routerParams.task, routerParams.difficulty, routerParams.type]);

  const {
    currentQuestion,
    currentQuestionIndex,
    selectedAnswer,
    showResult,
    isCorrect,
    stats,
    filteredQuestions,
    loading,
    progress,
    isLastQuestion,
    selectAnswer,
    submitAnswer,
    nextQuestion,
    previousQuestion,
    restartQuiz,
    availableTaskStatements,
    questionService,
  } = useQuiz(allQuestions, quizOptions);

  // Handle loading state
  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading questions...</Text>
        </View>
      </SafeAreaView>
    );
  }

  // Handle case when no questions match the filter
  if (filteredQuestions.length === 0) {
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
          <QuizFilters
            availableTaskStatements={availableTaskStatements as string[]}
            isVisible={showFilters}
            onToggleVisibility={() => setShowFilters(!showFilters)}
          />
          <View style={styles.noQuestionsContainer}>
            <Text style={styles.noQuestionsText}>
              No questions match the selected filters.
            </Text>
            <Text style={styles.noQuestionsSubtext}>
              Try adjusting your filter settings.
            </Text>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // Handle case when currentQuestion is undefined
  if (!currentQuestion) {
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
          <QuizFilters
            availableTaskStatements={availableTaskStatements as string[]}
            isVisible={showFilters}
            onToggleVisibility={() => setShowFilters(!showFilters)}
          />
          <View style={styles.noQuestionsContainer}>
            <Text style={styles.noQuestionsText}>
              Loading questions...
            </Text>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        <QuizFilters
          availableTaskStatements={availableTaskStatements as string[]}
          isVisible={showFilters}
          onToggleVisibility={() => setShowFilters(!showFilters)}
        />

        <ProgressBar
          currentQuestion={currentQuestionIndex + 1}
          totalQuestions={filteredQuestions.length}
          stats={stats}
        />

        {(routerParams.task || routerParams.difficulty || routerParams.type === 'unseen') && (
          <View style={styles.filterSummary}>
            <Text style={styles.filterSummaryText}>
              Filters: {[
                routerParams.task ? `Task ${routerParams.task}` : null,
                routerParams.difficulty ? routerParams.difficulty : null,
                routerParams.type === 'unseen' ? 'Unseen Questions' : null
              ].filter(Boolean).join(', ')}
            </Text>
          </View>
        )}

        <QuestionCard
          question={currentQuestion}
          selectedAnswer={selectedAnswer || undefined}
          onAnswerSelect={selectAnswer}
          showResult={showResult}
          isCorrect={isCorrect}
          getDifficultyColor={questionService.getDifficultyColor.bind(questionService)}
        />

        <QuizResults
          currentQuestion={currentQuestion}
          isCorrect={isCorrect}
          showResult={showResult}
          onNextQuestion={nextQuestion}
          onRestart={restartQuiz}
          isLastQuestion={isLastQuestion}
        />

        <View style={[styles.buttonContainer, { paddingBottom: Math.max(20, insets.bottom + 10) }]}>
          {!showResult && (
            <TouchableOpacity
              style={[styles.button, styles.submitButton]}
              onPress={submitAnswer}
            >
              <Text style={styles.buttonText}>Submit Answer</Text>
            </TouchableOpacity>
          )}
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
  scrollView: {
    flex: 1,
    padding: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  backButton: {
    padding: 8,
    backgroundColor: '#E3F2FD',
    borderRadius: 8,
    marginRight: 12,
  },
  backButtonText: {
    fontSize: 14,
    color: '#1976D2',
    fontWeight: '600',
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
  questionCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  questionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  taskStatement: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  difficultyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  difficultyText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  questionText: {
    fontSize: 18,
    lineHeight: 24,
    color: '#333',
    fontWeight: '500',
  },
  answersContainer: {
    marginBottom: 20,
  },
  answer: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'flex-start',
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedAnswer: {
    backgroundColor: '#E3F2FD',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'flex-start',
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    borderWidth: 2,
    borderColor: '#2196F3',
  },
  correctAnswer: {
    backgroundColor: '#E8F5E8',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'flex-start',
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  incorrectAnswer: {
    backgroundColor: '#FFEBEE',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'flex-start',
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    borderWidth: 2,
    borderColor: '#F44336',
  },
  answerLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginRight: 12,
    width: 20,
  },
  answerText: {
    fontSize: 16,
    color: '#333',
    flex: 1,
    lineHeight: 22,
  },
  resultContainer: {
    marginBottom: 20,
  },
  resultHeader: {
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  resultText: {
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
  },
  explanationContainer: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  explanationTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  explanationText: {
    fontSize: 15,
    lineHeight: 22,
    color: '#555',
  }, buttonContainer: {
    gap: 12,
    marginBottom: 40,
  },
  button: {
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  submitButton: {
    backgroundColor: '#2196F3',
  },
  nextButton: {
    backgroundColor: '#4CAF50',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  loadingText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
    textAlign: 'center',
  },
  noQuestionsContainer: {
    padding: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  noQuestionsText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
    textAlign: 'center',
    marginBottom: 8,
  }, noQuestionsSubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
  filterSummary: {
    backgroundColor: '#E3F2FD',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    marginBottom: 16,
  },
  filterSummaryText: {
    fontSize: 14,
    color: '#1976D2',
    textAlign: 'center',
    fontWeight: '500',
  },
});

export default Quiz;
