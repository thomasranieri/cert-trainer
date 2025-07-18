import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Question } from '../types';

interface QuestionCardProps {
  question: Question;
  selectedAnswer?: string;
  onAnswerSelect: (answer: string) => void;
  showResult: boolean;
  isCorrect?: boolean;
  getDifficultyColor: (difficulty: string) => string;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  selectedAnswer,
  onAnswerSelect,
  showResult,
  isCorrect,
  getDifficultyColor
}) => {
  const getAnswerStyle = (answer: string) => {
    if (!showResult) {
      return selectedAnswer === answer ? styles.selectedAnswer : styles.answer;
    }

    if (answer === question.correct) {
      return styles.correctAnswer;
    }

    if (selectedAnswer === answer && answer !== question.correct) {
      return styles.incorrectAnswer;
    }

    return styles.answer;
  };

  return (
    <View style={styles.questionCard}>
      <View style={styles.questionHeader}>
        <Text style={styles.taskStatement}>Task: {question.taskStatement}</Text>
        <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(question.difficulty || 'MEDIUM') }]}>
          <Text style={styles.difficultyText}>{question.difficulty || 'MEDIUM'}</Text>
        </View>
      </View>
      
      <Text style={styles.questionText}>{question.stem}</Text>
      
      <View style={styles.answersContainer}>
        {Object.entries(question.answers).map(([key, value]) => (
          <TouchableOpacity
            key={key}
            style={getAnswerStyle(key)}
            onPress={() => onAnswerSelect(key)}
            disabled={showResult}
          >
            <Text style={styles.answerLabel}>{String(key)}.</Text>
            <Text style={styles.answerText}>{value !== undefined && value !== null ? String(value) : ''}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
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
    marginBottom: 20,
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
});
