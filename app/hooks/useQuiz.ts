import { useCallback, useEffect, useMemo, useState } from 'react';
import { Alert } from 'react-native';
import { databaseService } from '../services/DatabaseService';
import { QuestionService } from '../services/QuestionService';
import { Question, QuizStats } from '../types';

export interface UseQuizOptions {
  selectedExam: string;
  task?: string;
  difficulty?: string;
  type?: 'all' | 'unseen';
}

export const useQuiz = (questions: Question[], options: UseQuizOptions) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [stats, setStats] = useState<QuizStats>({ total: 0, correct: 0, percentage: 0 });
  const [seenQuestionHashes, setSeenQuestionHashes] = useState<Set<string>>(new Set());
  const [filteredQuestions, setFilteredQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);

  const questionService = useMemo(() => new QuestionService(questions), [questions]);
  
  const loadStats = useCallback(async () => {
    try {
      const currentStats = await databaseService.getStats(options.selectedExam);
      setStats(currentStats);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  }, [options.selectedExam]);

  const loadSeenQuestions = useCallback(async () => {
    try {
      const history = await databaseService.getQuizHistory(options.selectedExam);
      const seenIds = new Set(history.map(activity => activity.questionId));
      setSeenQuestionHashes(seenIds);
    } catch (error) {
      console.error('Error loading seen questions:', error);
    }
  }, [options.selectedExam]);

  const resetQuizState = useCallback(() => {
    setCurrentQuestionIndex(0);
    setSelectedAnswer(null);
    setShowResult(false);
    setIsCorrect(false);
  }, []);
  
  const currentQuestion = useMemo(() => filteredQuestions[currentQuestionIndex], [filteredQuestions, currentQuestionIndex]);
  
  const isLastQuestion = currentQuestionIndex === filteredQuestions.length - 1;
  const progress = filteredQuestions.length > 0 ? ((currentQuestionIndex + 1) / filteredQuestions.length) * 100 : 0;

  // Initialize database and load data
  useEffect(() => {
    const initialize = async () => {
      try {
        await databaseService.initialize();
        await loadStats();
        await loadSeenQuestions();
      } catch (error) {
        console.error('Error initializing quiz:', error);
      } finally {
        setLoading(false);
      }
    };

    initialize();
  }, [options.selectedExam, loadStats, loadSeenQuestions]);

  // Filter questions based on options
  useEffect(() => {
    if (loading) return;

    let filtered = questionService.getQuestionsByExam(options.selectedExam);

    if (options.task) {
      filtered = filtered.filter((q: Question) => q.taskStatement === options.task);
    }

    if (options.difficulty) {
      filtered = filtered.filter((q: Question) => q.difficulty === options.difficulty);
    }

    if (options.type === 'unseen') {
      filtered = filtered.filter((q: Question) => q.id !== undefined && !seenQuestionHashes.has(q.id));
    }

    // Shuffle the filtered questions
    const shuffled = questionService.shuffleQuestions(filtered);
    setFilteredQuestions(shuffled);
    resetQuizState();
  }, [
    loading,
    options.selectedExam,
    options.task,
    options.difficulty,
    options.type,
    seenQuestionHashes,
    questionService,
    resetQuizState
  ]);

  const selectAnswer = useCallback((answer: string) => {
    if (showResult) return;
    setSelectedAnswer(answer);
  }, [showResult]);

  const submitAnswer = useCallback(async () => {
    if (!selectedAnswer || !currentQuestion) {
      Alert.alert('Please select an answer', 'You must choose an answer before submitting.');
      return;
    }

    const correct = selectedAnswer === currentQuestion.correct;
    setIsCorrect(correct);
    setShowResult(true);

    // Save to database
    try {
      await databaseService.saveQuizActivity({
        questionIndex: currentQuestionIndex,
        exam: options.selectedExam,
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
    } catch (error) {
      console.error('Error saving quiz activity:', error);
    }
  }, [selectedAnswer, currentQuestion, currentQuestionIndex, options.selectedExam, loadStats]);

  const nextQuestion = useCallback(() => {
    if (isLastQuestion) {
      const finalScore = stats.correct + (isCorrect ? 1 : 0);
      const finalTotal = stats.total + 1;
      const finalPercentage = Math.round((finalScore / finalTotal) * 100);

      Alert.alert(
        'Quiz Complete!',
        `Your overall score: ${finalScore}/${finalTotal} (${finalPercentage}%)`,
        [
          {
            text: 'Restart',
            onPress: resetQuizState,
          },
        ]
      );
    } else {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowResult(false);
      setIsCorrect(false);
    }
  }, [isLastQuestion, stats, isCorrect, resetQuizState]);

  const previousQuestion = useCallback(() => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
      setSelectedAnswer(null);
      setShowResult(false);
      setIsCorrect(false);
    }
  }, [currentQuestionIndex]);

  const restartQuiz = useCallback(() => {
    resetQuizState();
  }, [resetQuizState]);

  const availableTaskStatements = useMemo((): string[] => {
    const examQuestions = questionService.getQuestionsByExam(options.selectedExam);
    return [...new Set(examQuestions.map((q: Question) => q.taskStatement))].sort() as string[];
  }, [questionService, options.selectedExam]);

  return {
    // State
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
    
    // Actions
    selectAnswer,
    submitAnswer,
    nextQuestion,
    previousQuestion,
    restartQuiz,
    
    // Computed values
    availableTaskStatements,
    
    // Utilities
    questionService,
  };
};
