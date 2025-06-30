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
import { databaseService, QuizActivity } from '../../services/DatabaseService';

const Stats: React.FC = () => {
  const [history, setHistory] = useState<QuizActivity[]>([]);
  const [stats, setStats] = useState({ total: 0, correct: 0, percentage: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [historyData, statsData] = await Promise.all([
        databaseService.getQuizHistory(), // TODO: incorporate exam filter when passing it via props or context
        databaseService.getStats(), // TODO: incorporate exam filter
      ]);
      setHistory(historyData);
      setStats(statsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = () => {
    Alert.alert(
      'Clear History',
      'Are you sure you want to clear all quiz history? This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Clear', style: 'destructive', onPress: async () => {
            await databaseService.clearHistory(); // TODO: pass exam filter if applicable
            setHistory([]);
            setStats({ total: 0, correct: 0, percentage: 0 });
          },
        },
      ]
    );
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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

  const getStatsByDifficulty = () => {
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

  const getStatsByTask = () => {
    // Collect all unique taskStatements from history
    const tasks = Array.from(new Set(history.map(h => h.taskStatement)));
    return tasks.map(taskStatement => {
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
    });
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading stats...</Text>
        </View>
      </SafeAreaView>
    );
  }

  const difficultyStats = getStatsByDifficulty();
  const taskStats = getStatsByTask();

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Overall Stats */}
        <View style={styles.statsCard}>
          <Text style={styles.cardTitle}>Overall Performance</Text>
          <View style={styles.overallStats}>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{stats.total}</Text>
              <Text style={styles.statLabel}>Total Questions</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{stats.correct}</Text>
              <Text style={styles.statLabel}>Correct Answers</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={[styles.statNumber, { color: stats.percentage >= 70 ? '#4CAF50' : '#F44336' }]}>
                {stats.percentage}%
              </Text>
              <Text style={styles.statLabel}>Accuracy</Text>
            </View>
          </View>
        </View>

        {/* Difficulty Breakdown */}
        <View style={styles.statsCard}>
          <Text style={styles.cardTitle}>Performance by Difficulty</Text>
          {difficultyStats.map(({ difficulty, correct, total, percentage }) => (
            <View key={difficulty} style={styles.difficultyRow}>
              <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(difficulty) }]}>
                <Text style={styles.difficultyText}>{difficulty}</Text>
              </View>
              <View style={styles.difficultyStats}>
                <Text style={styles.difficultyStatsText}>
                  {correct}/{total} ({percentage}%)
                </Text>
              </View>
            </View>
          ))}
        </View>

        {/* Task Breakdown */}
        {taskStats.length > 0 && (
          <View style={styles.statsCard}>
            <Text style={styles.cardTitle}>Performance by Task</Text>
            {taskStats.map(({ taskStatement, correct, total, percentage }) => (
              <View key={taskStatement} style={styles.difficultyRow}>
                <View style={[styles.difficultyBadge, { backgroundColor: '#2196F3' }]}> 
                  <Text style={styles.difficultyText}>{taskStatement || 'Unknown'}</Text>
                </View>
                <View style={styles.difficultyStats}>
                  <Text style={styles.difficultyStatsText}>
                    {correct}/{total} ({percentage}%)
                  </Text>
                </View>
              </View>
            ))}
          </View>
        )}

        {/* Recent Activity */}
        <View style={styles.statsCard}>
          <View style={styles.cardHeader}>
            <Text style={styles.cardTitle}>Recent Activity</Text>
            {history.length > 0 && (
              <TouchableOpacity
                style={styles.clearButton}
                onPress={handleClearHistory}
              >
                <Text style={styles.clearButtonText}>Clear All</Text>
              </TouchableOpacity>
            )}
          </View>
          
          {history.length === 0 ? (
            <Text style={styles.emptyText}>No quiz activity yet. Start practicing to see your progress!</Text>
          ) : (
            history.slice(0, 20).map((activity, index) => (
              <View key={activity.id || index} style={styles.activityItem}>
                <View style={styles.activityHeader}>
                  <View style={styles.activityInfo}>
                    <View style={[styles.difficultyBadge, styles.smallBadge, { backgroundColor: getDifficultyColor(activity.difficulty) }]}>
                      <Text style={[styles.difficultyText, styles.smallBadgeText]}>{activity.difficulty}</Text>
                    </View>
                    <Text style={styles.taskText}>Task {activity.taskStatement}</Text>
                  </View>
                  <View style={[styles.resultBadge, { backgroundColor: activity.isCorrect ? '#E8F5E8' : '#FFEBEE' }]}>
                    <Text style={[styles.resultText, { color: activity.isCorrect ? '#2E7D32' : '#C62828' }]}>
                      {activity.isCorrect ? '✓' : '✗'}
                    </Text>
                  </View>
                </View>
                <Text style={styles.answerText}>
                  Selected: {activity.selectedAnswer} | Correct: {activity.correctAnswer}
                </Text>
                <Text style={styles.timestampText}>{formatDate(activity.timestamp)}</Text>
              </View>
            ))
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
  },
  statsCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  overallStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  difficultyRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  difficultyBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  smallBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  difficultyText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  smallBadgeText: {
    fontSize: 10,
  },
  difficultyStats: {
    flex: 1,
    alignItems: 'flex-end',
  },
  difficultyStatsText: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  clearButton: {
    backgroundColor: '#F44336',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  clearButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  emptyText: {
    textAlign: 'center',
    color: '#666',
    fontSize: 16,
    fontStyle: 'italic',
    paddingVertical: 20,
  },
  activityItem: {
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    paddingVertical: 12,
  },
  activityHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  activityInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  taskText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
  },
  resultBadge: {
    width: 24,
    height: 24,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  resultText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  answerText: {
    fontSize: 14,
    color: '#333',
    marginBottom: 4,
  },
  timestampText: {
    fontSize: 12,
    color: '#999',
  },
});

export default Stats;
