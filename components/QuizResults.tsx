import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Question } from '../types';

interface QuizResultsProps {
  currentQuestion: Question;
  isCorrect: boolean;
  showResult: boolean;
  onNextQuestion: () => void;
  onRestart: () => void;
  isLastQuestion: boolean;
}

export const QuizResults: React.FC<QuizResultsProps> = ({
  currentQuestion,
  isCorrect,
  showResult,
  onNextQuestion,
  onRestart,
  isLastQuestion
}) => {
  const openAIExplanation = () => {
    window.open(`https://chatgpt.com/?q=${encodeURIComponent(`Explain the answer to the question: ${currentQuestion.stem} with options ${JSON.stringify(currentQuestion.answers)}`)}`);
  };

  if (!showResult) return null;

  return (
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

      <View style={styles.buttonContainer}>
        {isLastQuestion ?
          <TouchableOpacity
            style={[styles.button, styles.restartButton]}
            onPress={onRestart}
          >
            <Text style={styles.buttonText}>
              You finished the quiz! Restart?
            </Text>
          </TouchableOpacity>
          :
          <TouchableOpacity
            style={[styles.button, styles.nextButton]}
            onPress={onNextQuestion}
          >
            <Text style={styles.buttonText}>
              Next Question
            </Text>
          </TouchableOpacity>}


        <TouchableOpacity
          style={[styles.button, styles.aiButton]}
          onPress={openAIExplanation}
        >
          <Text style={styles.buttonText}>Further Explanation</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
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
    marginBottom: 20,
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
  },
  buttonContainer: {
    gap: 12,
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
  nextButton: {
    backgroundColor: '#4CAF50',
  },
  aiButton: {
    backgroundColor: '#2196F3',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  restartButton: {
    backgroundColor: '#FF9800',
  },
});
