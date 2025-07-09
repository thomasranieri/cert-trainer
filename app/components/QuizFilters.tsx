import React from 'react';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

interface QuizFiltersProps {
  selectedTaskStatement: string | null;
  selectedDifficulty: string | null;
  selectedQuestionType: 'all' | 'unseen' | null;
  onTaskStatementChange: (taskStatement: string | null) => void;
  onDifficultyChange: (difficulty: string | null) => void;
  onQuestionTypeChange: (questionType: 'all' | 'unseen' | null) => void;
  availableTaskStatements: string[];
  isVisible: boolean;
  onToggleVisibility: () => void;
}

const QuizFilters: React.FC<QuizFiltersProps> = ({
  selectedTaskStatement,
  selectedDifficulty,
  selectedQuestionType,
  onTaskStatementChange,
  onDifficultyChange,
  onQuestionTypeChange,
  availableTaskStatements,
  isVisible,
  onToggleVisibility,
}) => {
  const difficulties = ['EASY', 'MEDIUM', 'HARD'];

  const getFilterButtonStyle = (isSelected: boolean) => [
    styles.filterButton,
    isSelected && styles.selectedFilterButton,
  ];

  const getFilterTextStyle = (isSelected: boolean) => [
    styles.filterText,
    isSelected && styles.selectedFilterText,
  ];

  return (
    <View style={styles.container}>
      {/* Toggle Button */}
      <TouchableOpacity
        style={styles.toggleButton}
        onPress={onToggleVisibility}
      >
        <Text style={styles.toggleButtonText}>
          {isVisible ? '▼ Hide Filters' : '▶ Show Filters'}
        </Text>
      </TouchableOpacity>

      {/* Filters */}
      {isVisible && (
        <View style={styles.filtersContainer}>
          {/* Task Statement Filter */}
          <View style={styles.filterSection}>
            <Text style={styles.filterTitle}>Task Statement:</Text>
            <View style={styles.filterOptions}>
              <TouchableOpacity
                style={getFilterButtonStyle(selectedTaskStatement === null)}
                onPress={() => onTaskStatementChange(null)}
              >
                <Text style={getFilterTextStyle(selectedTaskStatement === null)}>
                  All Tasks
                </Text>
              </TouchableOpacity>
              {availableTaskStatements.map((task) => (
                <TouchableOpacity
                  key={task}
                  style={getFilterButtonStyle(selectedTaskStatement === task)}
                  onPress={() => onTaskStatementChange(task)}
                >
                  <Text style={getFilterTextStyle(selectedTaskStatement === task)}>
                    Task {task}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Difficulty Filter */}
          <View style={styles.filterSection}>
            <Text style={styles.filterTitle}>Difficulty:</Text>
            <View style={styles.filterOptions}>
              <TouchableOpacity
                style={getFilterButtonStyle(selectedDifficulty === null)}
                onPress={() => onDifficultyChange(null)}
              >
                <Text style={getFilterTextStyle(selectedDifficulty === null)}>
                  All Levels
                </Text>
              </TouchableOpacity>
              {difficulties.map((difficulty) => (
                <TouchableOpacity
                  key={difficulty}
                  style={getFilterButtonStyle(selectedDifficulty === difficulty)}
                  onPress={() => onDifficultyChange(difficulty)}
                >
                  <Text style={getFilterTextStyle(selectedDifficulty === difficulty)}>
                    {difficulty}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Question Type Filter */}
          <View style={styles.filterSection}>
            <Text style={styles.filterTitle}>Question Type:</Text>
            <View style={styles.filterOptions}>
              <TouchableOpacity
                style={getFilterButtonStyle(selectedQuestionType === null || selectedQuestionType === 'all')}
                onPress={() => onQuestionTypeChange('all')}
              >
                <Text style={getFilterTextStyle(selectedQuestionType === null || selectedQuestionType === 'all')}>
                  All Questions
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={getFilterButtonStyle(selectedQuestionType === 'unseen')}
                onPress={() => onQuestionTypeChange('unseen')}
              >
                <Text style={getFilterTextStyle(selectedQuestionType === 'unseen')}>
                  Unseen Questions
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'white',
    borderRadius: 12,
    marginBottom: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  toggleButton: {
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  toggleButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2196F3',
  },
  filtersContainer: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  filterSection: {
    marginBottom: 16,
  },
  filterTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  filterOptions: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  filterButton: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    backgroundColor: '#f5f5f5',
    borderWidth: 1,
    borderColor: '#ddd',
  },
  selectedFilterButton: {
    backgroundColor: '#2196F3',
    borderColor: '#2196F3',
  },
  filterText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#666',
  },
  selectedFilterText: {
    color: 'white',
  },
});

export default QuizFilters;
