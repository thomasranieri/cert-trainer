import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Question } from '../types';

interface QuestionCardProps {
  question: Question;
  // MCQ
  selectedAnswer?: string;
  onAnswerSelect: (answer: string) => void;
  // MAMCQ
  selectedAnswers?: string[];
  onAnswerToggle?: (answer: string) => void;
  // MATCH
  matchSelections?: Record<string, string>;
  onMatchSelect?: (subId: string, answerKey: string) => void;
  // Common
  showResult: boolean;
  isCorrect?: boolean;
  getDifficultyColor: (difficulty: string) => string;
}

export const QuestionCard: React.FC<QuestionCardProps> = (props) => {
  const {
    question,
    selectedAnswer,
    onAnswerSelect,
    onAnswerToggle,
    onMatchSelect,
    showResult,
    isCorrect,
    getDifficultyColor,
  } = props;
  const selectedAnswers: string[] = props.selectedAnswers ?? [];
  const matchSelections: Record<string, string> = props.matchSelections ?? {};
  const questionType = question.type ?? 'MCQ';

  const getMCQAnswerStyle = (key: string) => {
    if (!showResult) {
      return selectedAnswer === key ? styles.selectedAnswer : styles.answer;
    }
    if (key === question.correct) return styles.correctAnswer;
    if (selectedAnswer === key) return styles.incorrectAnswer;
    return styles.answer;
  };

  const getMAMCQAnswerStyle = (key: string) => {
    const isSelected = selectedAnswers.includes(key);
    const correct = question.correct as string[];
    if (!showResult) {
      return isSelected ? styles.selectedAnswer : styles.answer;
    }
    if (correct.includes(key)) return styles.correctAnswer;
    if (isSelected) return styles.incorrectAnswer;
    return styles.answer;
  };

  const getMatchOptionStyle = (subId: string, key: string) => {
    const isSelected = matchSelections[subId] === key;
    const sub = question.subquestions?.find(s => s.id === subId);
    if (!showResult) {
      return isSelected ? styles.matchOptionSelected : styles.matchOption;
    }
    if (key === sub?.correct) return styles.matchOptionCorrect;
    if (isSelected) return styles.matchOptionIncorrect;
    return styles.matchOption;
  };

  const renderHeader = () => (
    <View style={styles.questionHeader}>
      {question.taskStatement ? (
        <Text style={styles.taskStatement}>Task: {question.taskStatement}</Text>
      ) : (
        <View />
      )}
      <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(question.difficulty ?? 'MEDIUM') }]}>
        <Text style={styles.difficultyText}>{question.difficulty ?? 'MEDIUM'}</Text>
      </View>
    </View>
  );

  if (questionType === 'MAMCQ') {
    const correct = (question.correct as string[]) ?? [];
    return (
      <View style={styles.questionCard}>
        {renderHeader()}
        <Text style={styles.questionText}>{question.stem}</Text>
        <View style={styles.answersContainer}>
          {Object.entries(question.answers).map(([key, value]) => {
            const isSelected = selectedAnswers.includes(key);
            return (
              <TouchableOpacity
                key={key}
                style={getMAMCQAnswerStyle(key)}
                onPress={() => onAnswerToggle?.(key)}
                disabled={showResult}
              >
                <View style={[styles.checkbox, isSelected && !showResult && styles.checkboxSelected,
                  showResult && correct.includes(key) && styles.checkboxCorrect,
                  showResult && isSelected && !correct.includes(key) && styles.checkboxIncorrect,
                ]}>
                  {isSelected && <Text style={styles.checkmark}>✓</Text>}
                </View>
                <Text style={styles.answerLabel}>{key}.</Text>
                <Text style={styles.answerText}>{String(value ?? '')}</Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </View>
    );
  }

  if (questionType === 'MATCH') {
    return (
      <View style={styles.questionCard}>
        {renderHeader()}
        <Text style={styles.questionText}>{question.stem}</Text>

        {question.subquestions?.map(sub => (
          <View key={sub.id} style={styles.matchSubQuestion}>
            <Text style={styles.matchPrompt}>{sub.prompt}</Text>
            <View style={styles.matchOptions}>
              {Object.entries(question.answers).map(([key, value]) => (
                <TouchableOpacity
                  key={key}
                  style={getMatchOptionStyle(sub.id, key)}
                  onPress={() => onMatchSelect?.(sub.id, key)}
                  disabled={showResult}
                >
                  <Text style={styles.matchOptionText}>{value}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        ))}
      </View>
    );
  }

  // Default: MCQ
  return (
    <View style={styles.questionCard}>
      {renderHeader()}
      <Text style={styles.questionText}>{question.stem}</Text>
      <View style={styles.answersContainer}>
        {Object.entries(question.answers).map(([key, value]) => (
          <TouchableOpacity
            key={key}
            style={getMCQAnswerStyle(key)}
            onPress={() => onAnswerSelect(key)}
            disabled={showResult}
          >
            <Text style={styles.answerLabel}>{key}.</Text>
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
  // MAMCQ checkbox styles
  checkbox: {
    width: 22,
    height: 22,
    borderRadius: 4,
    borderWidth: 2,
    borderColor: '#999',
    marginRight: 12,
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  checkboxSelected: {
    borderColor: '#2196F3',
    backgroundColor: '#2196F3',
  },
  checkboxCorrect: {
    borderColor: '#4CAF50',
    backgroundColor: '#4CAF50',
  },
  checkboxIncorrect: {
    borderColor: '#F44336',
    backgroundColor: '#F44336',
  },
  checkmark: {
    color: 'white',
    fontSize: 14,
    fontWeight: '700',
  },
  // MATCH styles
  matchSubQuestion: {
    marginBottom: 12,
    padding: 12,
    backgroundColor: '#FAFAFA',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  matchPrompt: {
    fontSize: 15,
    color: '#333',
    marginBottom: 10,
    lineHeight: 20,
  },
  matchOptions: {
    flexDirection: 'row',
    gap: 8,
    flexWrap: 'wrap',
  },
  matchOption: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#CCC',
    backgroundColor: 'white',
    alignItems: 'center',
    justifyContent: 'center',
  },
  matchOptionSelected: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#2196F3',
    backgroundColor: '#E3F2FD',
    alignItems: 'center',
    justifyContent: 'center',
  },
  matchOptionCorrect: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#4CAF50',
    backgroundColor: '#E8F5E8',
    alignItems: 'center',
    justifyContent: 'center',
  },
  matchOptionIncorrect: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#F44336',
    backgroundColor: '#FFEBEE',
    alignItems: 'center',
    justifyContent: 'center',
  },
  matchOptionText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#333',
  },
});
