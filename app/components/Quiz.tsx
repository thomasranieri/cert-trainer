import { useLocalSearchParams } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  Alert,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { databaseService, Question } from '../../services/DatabaseService';
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
  const [examQuestions, setExamQuestions] = useState<Question[]>([]);
  const [filteredQuestions, setFilteredQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [stats, setStats] = useState({ total: 0, correct: 0, percentage: 0 });

  const [showFilters, setShowFilters] = useState(false);
  const [seenQuestionHashes, setSeenQuestionHashes] = useState<Set<string>>(new Set());
  const availableTaskStatements = [...new Set(examQuestions.map(q => q.taskStatement))].sort();

  // Function to shuffle array using Fisher-Yates algorithm
  const shuffleArray = <T,>(array: T[]): T[] => {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  };

  useEffect(() => {
    initializeDatabase();
    loadStats();
    loadSeenQuestions();
  }, []);

  // Filter questions by selected exam
  useEffect(() => {
    const questionsForExam = allQuestions.filter(q => q.exam === routerParams.exam);
    setExamQuestions(questionsForExam);
  }, [allQuestions, routerParams.exam]);

  // Filter questions based on selected criteria
  useEffect(() => {
    let filtered = examQuestions;

    if (routerParams.task) {
      filtered = filtered.filter(q => q.taskStatement === routerParams.task);
    }

    if (routerParams.difficulty) {
      filtered = filtered.filter(q => q.difficulty === routerParams.difficulty);
    }

    if (routerParams.type === 'unseen') {
      filtered = filtered.filter(q => q.id !== undefined && !seenQuestionHashes.has(q.id));
    }

    // Shuffle the filtered questions to display them in random order
    const shuffledFiltered = shuffleArray(filtered);

    setFilteredQuestions(shuffledFiltered);
    setCurrentQuestionIndex(0);
    setSelectedAnswer(null);
    setShowResult(false);
    setIsCorrect(false);
  }, [routerParams.task, routerParams.difficulty, routerParams.type, examQuestions, seenQuestionHashes]);

  const initializeDatabase = async () => {
    await databaseService.initialize();
  };

  const loadStats = async () => {
    const currentStats = await databaseService.getStats(selectedExam);
    setStats(currentStats);
  };

  const loadSeenQuestions = async () => {
    const history = await databaseService.getQuizHistory(selectedExam);
    const seenIds = new Set(history.map(activity => activity.questionId));
    setSeenQuestionHashes(seenIds);
  };

  const openAIExplanation = () => {
    window.open(`https://chatgpt.com/?q=${encodeURIComponent(`Explain the answer to the question: ${filteredQuestions[currentQuestionIndex].stem} with options ${JSON.stringify(filteredQuestions[currentQuestionIndex].answers)}`)}`);
  }

  const currentQuestion = filteredQuestions[currentQuestionIndex];

  // Handle case when no questions match the filter
  if (filteredQuestions.length === 0) {
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
          <QuizFilters
            availableTaskStatements={availableTaskStatements}
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
            availableTaskStatements={availableTaskStatements}
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
  }

  const handleAnswerSelect = (answer: string) => {
    if (showResult) return;
    setSelectedAnswer(answer);
  };

  const handleSubmitAnswer = async () => {
    if (!selectedAnswer) {
      Alert.alert('Please select an answer', 'You must choose an answer before submitting.');
      return;
    }

    const correct = selectedAnswer === currentQuestion.correct;
    setIsCorrect(correct);
    setShowResult(true);

    // Save to database
    await databaseService.saveQuizActivity({
      questionIndex: currentQuestionIndex,
      exam: selectedExam,  // include exam filter
      selectedAnswer,
      correctAnswer: currentQuestion.correct,
      isCorrect: correct,
      timestamp: new Date().toISOString(),
      difficulty: currentQuestion.difficulty || 'MEDIUM',
      taskStatement: currentQuestion.taskStatement,
      questionId: currentQuestion.id || 'UNKNOWN'
    });

    // Update stats
    await loadStats();
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
      setShowResult(false);
      setIsCorrect(false);
    } else {
      Alert.alert(
        'Quiz Complete!',
        `You've completed all questions! Your overall score: ${stats.correct + (isCorrect ? 1 : 0)}/${stats.total + 1} (${Math.round(((stats.correct + (isCorrect ? 1 : 0)) / (stats.total + 1)) * 100)}%)`,
        [
          {
            text: 'Restart',
            onPress: () => {
              setCurrentQuestionIndex(0);
              setSelectedAnswer(null);
              setShowResult(false);
              setIsCorrect(false);
            },
          },
        ]
      );
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'EASY':
        return '#4CAF50';
      case 'MEDIUM':
        return '#FF9800';
      case 'HARD':
        return '#F44336';
      default:
        return '#757575';
    }
  };

  const getAnswerStyle = (answer: string) => {
    if (!showResult) {
      return selectedAnswer === answer ? styles.selectedAnswer : styles.answer;
    }

    if (answer === currentQuestion.correct) {
      return styles.correctAnswer;
    }

    if (selectedAnswer === answer && answer !== currentQuestion.correct) {
      return styles.incorrectAnswer;
    }

    return styles.answer;
  };
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        <QuizFilters
          availableTaskStatements={availableTaskStatements}
          isVisible={showFilters}
          onToggleVisibility={() => setShowFilters(!showFilters)}
        />

        <View style={styles.header}>
          <Text style={styles.questionCounter}>
            Question {currentQuestionIndex + 1} of {filteredQuestions.length}
          </Text>
          <View style={styles.statsContainer}>
            <Text style={styles.stats}>
              Score: {stats.correct}/{stats.total} ({stats.percentage}%)
            </Text>
          </View>
        </View>

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

        <View style={styles.questionCard}>
          <View style={styles.questionHeader}>
            <Text style={styles.taskStatement}>Task: {currentQuestion.taskStatement}</Text>
            <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(currentQuestion.difficulty || 'MEDIUM') }]}>
              <Text style={styles.difficultyText}>{currentQuestion.difficulty || 'MEDIUM'}</Text>
            </View>
          </View>

          <Text style={styles.questionText}>{currentQuestion.stem}</Text>
        </View>

        <View style={styles.answersContainer}>
          {Object.entries(currentQuestion.answers).map(([key, value]) => (
            <TouchableOpacity
              key={key}
              style={getAnswerStyle(key)}
              onPress={() => handleAnswerSelect(key)}
              disabled={showResult}
            >
              <Text style={styles.answerLabel}>{String(key)}.</Text>
              <Text style={styles.answerText}>{value !== undefined && value !== null ? String(value) : ''}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {showResult && (
          <View style={styles.resultContainer}>
            <View style={[styles.resultHeader, { backgroundColor: isCorrect ? '#E8F5E8' : '#FFEBEE' }]}>
              <Text style={[styles.resultText, { color: isCorrect ? '#2E7D32' : '#C62828' }]}>
                {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
              </Text>
            </View>

            <View style={styles.explanationContainer}>
              <Text style={styles.explanationTitle}>Explanation:</Text>
              <Text style={styles.explanationText}>{currentQuestion.explanation}</Text>
            </View>
          </View>
        )}
        <View style={[styles.buttonContainer, { paddingBottom: Math.max(20, insets.bottom + 10) }]}>
          {!showResult ? (
            <TouchableOpacity
              style={[styles.button, styles.submitButton]}
              onPress={handleSubmitAnswer}
            >
              <Text style={styles.buttonText}>Submit Answer</Text>
            </TouchableOpacity>
          ) : (
            <>
              <TouchableOpacity
                style={[styles.button, styles.nextButton]}
                onPress={handleNextQuestion}
              >
                <Text style={styles.buttonText}>
                  {currentQuestionIndex < filteredQuestions.length - 1 ? 'Next Question' : 'Complete Quiz'}
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.button}
                onPress={openAIExplanation}
              >
                <Text style={[styles.button]}>Further Explanation</Text>
              </TouchableOpacity>
            </>
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
