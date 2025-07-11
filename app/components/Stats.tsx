import { Link, router } from 'expo-router';
import React, { useState } from 'react';
import {
  Modal,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useStats } from '../../hooks/useStats';
import { Question } from '../../types';
import questionsData from '../data/questions.json';

// Add props for selected exam
interface StatsProps {
  selectedExam: string;
}

// Modify component signature to accept selectedExam
const Stats: React.FC<StatsProps> = ({ selectedExam }) => {
  const [allQuestions] = useState<Question[]>(questionsData as Question[]);
  
  const {
    history,
    stats,
    loading,
    selectedQuestionDetail,
    showDetailModal,
    clearHistory,
    handleActivityPress,
    closeDetailModal,
    difficultyStats,
    taskStats,
    formatDate,
    getDifficultyColor,
  } = useStats(selectedExam, allQuestions);

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading stats...</Text>
        </View>
      </SafeAreaView>
    );
  }

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
              <Link key={difficulty} href={{ pathname: '/quiz', params: { exam: selectedExam, difficulty } }}>
                <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(difficulty) }]}>
                  <Text style={styles.difficultyText}>{difficulty}</Text>
                </View>
              </Link>
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
            <View style={styles.tableHeader}>
              <Text style={styles.tableHeaderText}>Task</Text>
              <Text style={styles.tableHeaderText}>Performance</Text>
            </View>
            {taskStats.map(({ taskStatement, correct, total, percentage }) => (
              <TouchableOpacity
                key={taskStatement}
                onPress={() => {
                  router.push({
                    pathname: '/quiz',
                    params: { exam: selectedExam, task: taskStatement },
                  });
                }}
              >
                <View style={styles.tableRow}>
                  <Text style={styles.tableCell}>{taskStatement || 'Unknown'}</Text>
                  <Text style={styles.tableCellRight}>
                    {correct}/{total} ({percentage}%)
                  </Text>
                </View>
              </TouchableOpacity>
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
                onPress={clearHistory}
              >
                <Text style={styles.clearButtonText}>Clear All</Text>
              </TouchableOpacity>
            )}
          </View>
          {history.length === 0 ? (
            <Text style={styles.emptyText}>No quiz activity yet. Start practicing to see your progress!</Text>
          ) : (
            history.slice(0, 20).map((activity, index) => (
              <TouchableOpacity key={activity.questionId || index} style={styles.activityItem} onPress={() => handleActivityPress(activity)}>
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
              </TouchableOpacity>
            ))
          )}
        </View>
        {/* Detail Modal */}
        {selectedQuestionDetail && (
          <Modal visible={showDetailModal} animationType="slide" onRequestClose={closeDetailModal}>
            <SafeAreaView style={styles.modalContainer}>
              <ScrollView contentContainerStyle={styles.modalContent} showsVerticalScrollIndicator={false}>
                <Text style={styles.modalTitle}>Question Detail</Text>
                <Text style={styles.modalStem}>{selectedQuestionDetail.stem}</Text>
                {Object.entries(selectedQuestionDetail.answers).map(([key, value]) => (
                  <Text key={key} style={styles.modalAnswer}>{key}. {value}</Text>
                ))}
                <Text style={styles.modalExplanationTitle}>Explanation:</Text>
                <Text style={styles.modalExplanation}>{selectedQuestionDetail.explanation}</Text>
                <TouchableOpacity style={styles.modalCloseButton} onPress={closeDetailModal}>
                  <Text style={styles.modalCloseButtonText}>Close</Text>
                </TouchableOpacity>
              </ScrollView>
            </SafeAreaView>
          </Modal>
        )}
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
  modalContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  modalContent: {
    padding: 20,
    paddingBottom: 40,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  modalStem: {
    fontSize: 16,
    color: '#333',
    marginBottom: 12,
  },
  modalAnswer: {
    fontSize: 14,
    color: '#333',
    marginBottom: 8,
  },
  modalExplanationTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    marginTop: 12,
    marginBottom: 4,
  },
  modalExplanation: {
    fontSize: 14,
    color: '#333',
    marginBottom: 16,
  },
  modalCloseButton: {
    backgroundColor: '#2196F3',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    alignSelf: 'flex-end',
  },
  modalCloseButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  taskRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
    color: 'black'
  },
  taskText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
  },
  tableHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    borderBottomWidth: 2,
    borderBottomColor: '#e0e0e0',
    paddingBottom: 8,
    marginBottom: 8,
  },
  tableHeaderText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  tableRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  tableCell: {
    fontSize: 14,
    color: '#333',
    flex: 1,
    paddingRight: 8,
  },
  tableCellRight: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    textAlign: 'right',
  },
});

export default Stats;
