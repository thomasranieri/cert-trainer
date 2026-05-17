import AsyncStorage from '@react-native-async-storage/async-storage';

// Entire service now uses AsyncStorage only

export interface Question {
  id?: string;
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
  questionId: string;
  questionIndex: number;
  exam: string;
  selectedAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  timestamp: string;
  difficulty: string;
  taskStatement: string;
}

export interface ExportedQuizActivity extends QuizActivity {
  question: Question;
}

export interface QuizBackupData {
  version: number;
  exportedAt: string;
  quizHistory: ExportedQuizActivity[];
  skippedQuestionIds?: string[];
}

export type ImportMode = 'merge' | 'replace';

export interface ImportResult {
  imported: number;
  skipped: number;
  total: number;
}

class DatabaseService {
  private key = 'quizHistory';
  private backupVersion = 1;

  // No initialization needed for AsyncStorage
  async initialize() {}

  // Data is stored as JSON array under key

  private parseQuizHistory(value: string | null): QuizActivity[] {
    if (!value) {
      return [];
    }

    try {
      const parsed = JSON.parse(value);
      if (!Array.isArray(parsed)) {
        return [];
      }

      return parsed.filter((item): item is QuizActivity => this.isValidActivity(item));
    } catch {
      return [];
    }
  }

  private isValidActivity(activity: unknown): activity is QuizActivity {
    if (!activity || typeof activity !== 'object') {
      return false;
    }

    const candidate = activity as Partial<QuizActivity>;

    return typeof candidate.questionId === 'string'
      && typeof candidate.questionIndex === 'number'
      && typeof candidate.exam === 'string'
      && typeof candidate.selectedAnswer === 'string'
      && typeof candidate.correctAnswer === 'string'
      && typeof candidate.isCorrect === 'boolean'
      && typeof candidate.timestamp === 'string'
      && typeof candidate.difficulty === 'string'
      && typeof candidate.taskStatement === 'string';
  }

  private getActivityKey(activity: QuizActivity): string {
    return [
      activity.questionId,
      activity.exam,
      activity.selectedAnswer,
      activity.correctAnswer,
      activity.timestamp,
    ].join('::');
  }

  private getHistoryByExam(history: QuizActivity[], examFilter?: string): QuizActivity[] {
    if (!examFilter) {
      return history;
    }

    return history.filter(item => item.exam === examFilter);
  }

  async saveQuizActivity(activity: QuizActivity) {
    await this.initialize();
    // Read existing list
    const json = await AsyncStorage.getItem(this.key);
    const list = this.parseQuizHistory(json);
    list.unshift(activity);
    await AsyncStorage.setItem(this.key, JSON.stringify(list));
    return;
  }

  async getQuizHistory(examFilter?: string): Promise<QuizActivity[]> {
    await this.initialize();
    const json = await AsyncStorage.getItem(this.key);
    const list = this.parseQuizHistory(json);
    return this.getHistoryByExam(list, examFilter);
  }

  async getStats(examFilter?: string) {
    await this.initialize();
    const json = await AsyncStorage.getItem(this.key);
    const list = this.getHistoryByExam(this.parseQuizHistory(json), examFilter);
    const total = list.length;
    const correct = list.filter(q => q.isCorrect).length;
    return { total, correct, percentage: total ? Math.round((correct / total) * 100) : 0 };
  }

  async clearHistory(examFilter?: string) {
    await this.initialize();
    if (examFilter) {
      const json = await AsyncStorage.getItem(this.key);
      const list = this.parseQuizHistory(json);
      const filtered = list.filter(q => q.exam !== examFilter);
      await AsyncStorage.setItem(this.key, JSON.stringify(filtered));
    } else {
      await AsyncStorage.removeItem(this.key);
    }
    return;
  }

  async exportData(questions: Question[], examFilter?: string): Promise<QuizBackupData> {
    await this.initialize();

    const quizHistory = await this.getQuizHistory(examFilter);
    const questionById = new Map(
      questions
        .filter((question): question is Question & { id: string } => typeof question.id === 'string')
        .map(question => [question.id, question]),
    );

    const skippedQuestionIds = new Set<string>();

    const exportedHistory = quizHistory.flatMap((activity) => {
      const question = questionById.get(activity.questionId);
      if (!question) {
        skippedQuestionIds.add(activity.questionId);
        return [];
      }

      return [{
        ...activity,
        question,
      }];
    });

    return {
      version: this.backupVersion,
      exportedAt: new Date().toISOString(),
      quizHistory: exportedHistory,
      skippedQuestionIds: Array.from(skippedQuestionIds),
    };
  }

  async importData(rawData: unknown, mode: ImportMode = 'merge', examFilter?: string): Promise<ImportResult> {
    await this.initialize();

    const importedHistory = Array.isArray(rawData)
      ? rawData
      : ((rawData as Partial<QuizBackupData>)?.quizHistory ?? []);

    if (!Array.isArray(importedHistory)) {
      return { imported: 0, skipped: 0, total: 0 };
    }

    const normalized = importedHistory.filter((item): item is QuizActivity => this.isValidActivity(item));
    const filteredImport = this.getHistoryByExam(normalized, examFilter);
    const total = filteredImport.length;

    const currentRaw = await AsyncStorage.getItem(this.key);
    const currentHistory = this.parseQuizHistory(currentRaw);

    const baseHistory = mode === 'replace'
      ? this.getHistoryByExam(currentHistory, examFilter).length
        ? currentHistory.filter(item => item.exam !== examFilter)
        : (examFilter ? currentHistory : [])
      : currentHistory;

    const existingKeys = new Set(baseHistory.map(item => this.getActivityKey(item)));
    let skipped = 0;

    for (const activity of filteredImport) {
      const activityKey = this.getActivityKey(activity);
      if (existingKeys.has(activityKey)) {
        skipped += 1;
        continue;
      }

      existingKeys.add(activityKey);
      baseHistory.push(activity);
    }

    baseHistory.sort((a, b) => {
      const left = new Date(a.timestamp).getTime();
      const right = new Date(b.timestamp).getTime();
      return right - left;
    });

    await AsyncStorage.setItem(this.key, JSON.stringify(baseHistory));

    return {
      imported: total - skipped,
      skipped,
      total,
    };
  }
}

export const databaseService = new DatabaseService();
