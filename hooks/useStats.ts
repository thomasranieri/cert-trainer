import { useEffect, useState } from 'react';
import { Alert } from 'react-native';
import { databaseService } from '../services/DatabaseService';
import { QuestionService } from '../services/QuestionService';
import { DifficultyStats, Question, QuizActivity, QuizStats, TaskStats } from '../types';

export const useStats = (selectedExam: string, allQuestions: Question[]) => {
  const [history, setHistory] = useState<QuizActivity[]>([]);
  const [stats, setStats] = useState<QuizStats>({ total: 0, correct: 0, percentage: 0 });
  const [loading, setLoading] = useState(true);
  const [selectedQuestionDetail, setSelectedQuestionDetail] = useState<Question | null>(null);
  const [showDetailModal, setShowDetailModal] = useState(false);

  const questionService = new QuestionService(allQuestions);

  useEffect(() => {
    loadData();
  }, [selectedExam]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [historyData, statsData] = await Promise.all([
        databaseService.getQuizHistory(selectedExam),
        databaseService.getStats(selectedExam),
      ]);
      setHistory(historyData);
      setStats(statsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = () => {
    Alert.alert(
      'Clear History',
      'Are you sure you want to clear all quiz history? This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: async () => {
            try {
              await databaseService.clearHistory(selectedExam);
              setHistory([]);
              setStats({ total: 0, correct: 0, percentage: 0 });
            } catch (error) {
              console.error('Error clearing history:', error);
            }
          },
        },
      ]
    );
  };

  const getStatsByDifficulty = (): DifficultyStats[] => {
    const difficulties = ['EASY', 'MEDIUM', 'HARD'];
    return difficulties.map(difficulty => {
      const difficultyQuestions = history.filter(h => h.difficulty === difficulty);
      const correct = difficultyQuestions.filter(h => h.isCorrect).length;
      const total = difficultyQuestions.length;
      const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;

      return {
        difficulty,
        correct,
        total,
        percentage,
      };
    });
  };

  const getStatsByTask = (): TaskStats[] => {
    const taskStatements = [...new Set(history.map(h => h.taskStatement))];
    return taskStatements.map(taskStatement => {
      const taskQuestions = history.filter(h => h.taskStatement === taskStatement);
      const correct = taskQuestions.filter(h => h.isCorrect).length;
      const total = taskQuestions.length;
      const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;

      return {
        taskStatement,
        correct,
        total,
        percentage,
      };
    }).sort((a, b) => a.percentage - b.percentage);
  };

  const handleActivityPress = async (activity: QuizActivity) => {
    try {
      const examQuestions = questionService.getQuestionsByExam(selectedExam);
      const question = examQuestions.find(q => q.id === activity.questionId);
      
      if (question) {
        setSelectedQuestionDetail(question);
        setShowDetailModal(true);
      } else {
        Alert.alert('Question not found', 'Unable to locate full question details.');
      }
    } catch (error) {
      console.error('Error finding question details:', error);
      Alert.alert('Error', 'Unable to load question details.');
    }
  };

  const closeDetailModal = () => {
    setShowDetailModal(false);
    setSelectedQuestionDetail(null);
  };

  const formatDate = (timestamp: string): string => {
    const date = new Date(timestamp);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return {
    // State
    history,
    stats,
    loading,
    selectedQuestionDetail,
    showDetailModal,
    
    // Actions
    clearHistory,
    handleActivityPress,
    closeDetailModal,
    
    // Computed values
    difficultyStats: getStatsByDifficulty(),
    taskStats: getStatsByTask(),
    
    // Utilities
    formatDate,
    getDifficultyColor: questionService.getDifficultyColor.bind(questionService),
  };
};
