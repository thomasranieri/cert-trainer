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
  // MCQ
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  // MAMCQ
  const [selectedAnswers, setSelectedAnswers] = useState<string[]>([]);
  // MATCH
  const [matchSelections, setMatchSelections] = useState<Record<string, string>>({});

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
    setSelectedAnswers([]);
    setMatchSelections({});
    setShowResult(false);
    setIsCorrect(false);
  }, []);

  const currentQuestion = useMemo(() => filteredQuestions[currentQuestionIndex], [filteredQuestions, currentQuestionIndex]);

  const isLastQuestion = currentQuestionIndex === filteredQuestions.length - 1;
  const progress = filteredQuestions.length > 0 ? ((currentQuestionIndex + 1) / filteredQuestions.length) * 100 : 0;

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
    resetQuizState,
  ]);

  const selectAnswer = useCallback((answer: string) => {
    if (showResult) return;
    setSelectedAnswer(answer);
  }, [showResult]);

  const toggleAnswer = useCallback((answer: string) => {
    if (showResult) return;
    setSelectedAnswers(prev =>
      prev.includes(answer) ? prev.filter(a => a !== answer) : [...prev, answer]
    );
  }, [showResult]);

  const selectMatchAnswer = useCallback((subId: string, answerKey: string) => {
    if (showResult) return;
    setMatchSelections(prev => ({ ...prev, [subId]: answerKey }));
  }, [showResult]);

  const submitAnswer = useCallback(async () => {
    if (!currentQuestion) return;

    const questionType = currentQuestion.type ?? 'MCQ';
    let correct = false;
    let serializedSelected = '';
    let serializedCorrect = '';

    if (questionType === 'MCQ') {
      if (!selectedAnswer) {
        Alert.alert('Please select an answer', 'You must choose an answer before submitting.');
        return;
      }
      correct = selectedAnswer === currentQuestion.correct;
      serializedSelected = selectedAnswer;
      serializedCorrect = String(currentQuestion.correct ?? '');
    } else if (questionType === 'MAMCQ') {
      if (selectedAnswers.length === 0) {
        Alert.alert('Please select answers', 'You must choose at least one answer before submitting.');
        return;
      }
      const correctSet = new Set(currentQuestion.correct as string[]);
      const selectedSet = new Set(selectedAnswers);
      correct = correctSet.size === selectedSet.size && [...correctSet].every(a => selectedSet.has(a));
      serializedSelected = JSON.stringify([...selectedAnswers].sort());
      serializedCorrect = JSON.stringify([...(currentQuestion.correct as string[])].sort());
    } else if (questionType === 'MATCH') {
      const subs = currentQuestion.subquestions ?? [];
      const unanswered = subs.filter(s => !matchSelections[s.id]);
      if (unanswered.length > 0) {
        Alert.alert('Please answer all parts', 'You must match all items before submitting.');
        return;
      }
      correct = subs.every(s => matchSelections[s.id] === s.correct);
      serializedSelected = JSON.stringify(matchSelections);
      const correctMap = Object.fromEntries(subs.map(s => [s.id, s.correct]));
      serializedCorrect = JSON.stringify(correctMap);
    }

    setIsCorrect(correct);
    setShowResult(true);

    try {
      await databaseService.saveQuizActivity({
        questionIndex: currentQuestionIndex,
        exam: options.selectedExam,
        selectedAnswer: serializedSelected,
        correctAnswer: serializedCorrect,
        isCorrect: correct,
        timestamp: new Date().toISOString(),
        difficulty: currentQuestion.difficulty ?? 'MEDIUM',
        taskStatement: currentQuestion.taskStatement ?? '',
        questionId: currentQuestion.id ?? 'UNKNOWN',
      });

      await loadStats();
    } catch (error) {
      console.error('Error saving quiz activity:', error);
    }
  }, [
    selectedAnswer,
    selectedAnswers,
    matchSelections,
    currentQuestion,
    currentQuestionIndex,
    options.selectedExam,
    loadStats,
  ]);

  const nextQuestion = useCallback(() => {
    if (isLastQuestion) {
      const finalScore = stats.correct + (isCorrect ? 1 : 0);
      const finalTotal = stats.total + 1;
      const finalPercentage = Math.round((finalScore / finalTotal) * 100);

      Alert.alert(
        'Quiz Complete!',
        `Your overall score: ${finalScore}/${finalTotal} (${finalPercentage}%)`,
        [{ text: 'Restart', onPress: resetQuizState }]
      );
    } else {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setSelectedAnswers([]);
      setMatchSelections({});
      setShowResult(false);
      setIsCorrect(false);
    }
  }, [isLastQuestion, stats, isCorrect, resetQuizState]);

  const previousQuestion = useCallback(() => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
      setSelectedAnswer(null);
      setSelectedAnswers([]);
      setMatchSelections({});
      setShowResult(false);
      setIsCorrect(false);
    }
  }, [currentQuestionIndex]);

  const restartQuiz = useCallback(() => {
    resetQuizState();
  }, [resetQuizState]);

  const availableTaskStatements = useMemo((): string[] => {
    const examQuestions = questionService.getQuestionsByExam(options.selectedExam);
    return [...new Set(examQuestions.map((q: Question) => q.taskStatement ?? '').filter(Boolean))].sort() as string[];
  }, [questionService, options.selectedExam]);

  return {
    currentQuestion,
    currentQuestionIndex,
    selectedAnswer,
    selectedAnswers,
    matchSelections,
    showResult,
    isCorrect,
    stats,
    filteredQuestions,
    loading,
    progress,
    isLastQuestion,

    selectAnswer,
    toggleAnswer,
    selectMatchAnswer,
    submitAnswer,
    nextQuestion,
    previousQuestion,
    restartQuiz,

    availableTaskStatements,
    questionService,
  };
};
