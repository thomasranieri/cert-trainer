import AsyncStorage from '@react-native-async-storage/async-storage';

// Entire service now uses AsyncStorage only

export interface Question {
  taskStatement: string;
  exam?: string;
  stem: string;
  correct: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  answers: {
    A: string;
    B: string;
    C: string;
    D: string;
  };
  explanation: string;
}

export interface QuizActivity {
  id?: number;
  questionIndex: number;
  stemHash: string;
  exam: string;
  selectedAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  timestamp: string;
  difficulty: string;
  taskStatement: string;
}

class DatabaseService {
  private key = 'quizHistory';

  // No initialization needed for AsyncStorage
  async initialize() {}

  // Data is stored as JSON array under key

  async saveQuizActivity(activity: Omit<QuizActivity, 'id'>) {
    await this.initialize();
    // Read existing list
    const json = await AsyncStorage.getItem(this.key) || '[]';
    const list: Omit<QuizActivity,'id'>[] = JSON.parse(json);
    list.unshift(activity);
    await AsyncStorage.setItem(this.key, JSON.stringify(list));
    return;
  }

  async getQuizHistory(examFilter?: string): Promise<QuizActivity[]> {
    await this.initialize();
    const json = await AsyncStorage.getItem(this.key) || '[]';
    let list: QuizActivity[] = JSON.parse(json);
    if (examFilter) {
      list = list.filter(q => q.exam === examFilter);
    }
    return list;
  }

  async getStats(examFilter?: string) {
    await this.initialize();
    const json = await AsyncStorage.getItem(this.key) || '[]';
    let list: QuizActivity[] = JSON.parse(json);
    if (examFilter) {
      list = list.filter(q => q.exam === examFilter);
    }
    const total = list.length;
    const correct = list.filter(q => q.isCorrect).length;
    return { total, correct, percentage: total ? Math.round((correct/total)*100) : 0 };
  }

  async clearHistory(examFilter?: string) {
    await this.initialize();
    if (examFilter) {
      const json = await AsyncStorage.getItem(this.key) || '[]';
      const list: QuizActivity[] = JSON.parse(json);
      const filtered = list.filter(q => q.exam !== examFilter);
      await AsyncStorage.setItem(this.key, JSON.stringify(filtered));
    } else {
      await AsyncStorage.removeItem(this.key);
    }
    return;
  }
}

export const databaseService = new DatabaseService();
