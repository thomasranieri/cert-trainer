import { useLocalSearchParams, useRouter } from 'expo-router';
import React from 'react';
import {
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
} from 'react-native';

interface QuizFiltersProps {
  availableTaskStatements: string[];
  isVisible: boolean;
  onToggleVisibility: () => void;
}

type Params = { 
  exam?: string;
  task?: string;
  difficulty?: string;
  type?: 'all' | 'unseen';
};

const QuizFilters: React.FC<QuizFiltersProps> = ({
  availableTaskStatements,
  isVisible,
  onToggleVisibility,
}) => {
  const router = useRouter();
  const routerParams = useLocalSearchParams<Params>();
  const difficulties = ['EASY', 'MEDIUM', 'HARD'];

  const currentTask = typeof routerParams.task === 'string' ? routerParams.task : undefined;
  const currentDifficulty = typeof routerParams.difficulty === 'string' ? routerParams.difficulty : undefined;
  const currentType = typeof routerParams.type === 'string' ? routerParams.type : undefined;

  const getFilterButtonStyle = (isSelected: boolean) => [
    styles.filterButton,
    isSelected && styles.selectedFilterButton,
  ];

  const getFilterTextStyle = (isSelected: boolean) => [
    styles.filterText,
    isSelected && styles.selectedFilterText,
  ];

  const updateFilters = (
    task?: string,
    difficulty?: string,
    type?: 'all' | 'unseen'
  ) => {
    const params: Record<string, string> = {};

    Object.entries(routerParams).forEach(([key, value]) => {
      if (typeof value === 'string') {
        params[key] = value;
      }
    });

    if (task) {
      params.task = task;
    } else {
      delete params.task;
    }

    if (difficulty) {
      params.difficulty = difficulty;
    } else {
      delete params.difficulty;
    }

    if (type && type !== 'all') {
      params.type = type;
    } else {
      delete params.type;
    }

    router.replace({ pathname: '/quiz', params });
  };


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
                style={getFilterButtonStyle(!currentTask)}
                onPress={() => updateFilters(undefined, currentDifficulty, currentType)}
              >
                <Text style={getFilterTextStyle(!currentTask)}>
                  All Tasks
                </Text>
              </TouchableOpacity>
              {availableTaskStatements.map((task) => (
                <TouchableOpacity
                  key={task}
                  style={getFilterButtonStyle(currentTask === task)}
                  onPress={() => updateFilters(task, currentDifficulty, currentType)}
                >
                  <Text style={getFilterTextStyle(currentTask === task)}>
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
                style={getFilterButtonStyle(!currentDifficulty)}
                onPress={() => updateFilters(currentTask, undefined, currentType)}
              >
                <Text style={getFilterTextStyle(!currentDifficulty)}>
                  All Levels
                </Text>
              </TouchableOpacity>
              {difficulties.map((difficulty) => (
                <TouchableOpacity
                  key={difficulty}
                  style={getFilterButtonStyle(currentDifficulty === difficulty)}
                  onPress={() => updateFilters(currentTask, difficulty, currentType)}
                >
                  <Text style={getFilterTextStyle(currentDifficulty === difficulty)}>
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
                style={getFilterButtonStyle(!currentType || currentType === 'all')}
                onPress={() => updateFilters(currentTask, currentDifficulty, 'all')}
              >
                <Text style={getFilterTextStyle(!currentType || currentType === 'all')}>
                  All Questions
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={getFilterButtonStyle(currentType === 'unseen')}
                onPress={() => updateFilters(currentTask, currentDifficulty, 'unseen')}
              >
                <Text style={getFilterTextStyle(currentType === 'unseen')}>
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
