import * as SQLite from 'expo-sqlite';

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
  exam: string;  // added exam field
  selectedAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  timestamp: string;
  difficulty: string;
  taskStatement: string;
}

class DatabaseService {
  private db: SQLite.SQLiteDatabase | null = null;
  private initialized = false;

  async initialize() {
    if (this.initialized && this.db) {
      return;
    }

    try {
      // Use a simpler database name to avoid path issues
      this.db = await SQLite.openDatabaseAsync('quiz.db');
      await this.createTables();
      this.initialized = true;
      console.log('Database initialized successfully');
    } catch (error) {
      console.error('Error initializing database:', error);
      // Fallback: try to create database with different approach
      try {
        this.db = await SQLite.openDatabaseAsync('quiz.db', {
          enableChangeListener: false,
        });
        await this.createTables();
        this.initialized = true;
        console.log('Database initialized with fallback method');
      } catch (fallbackError) {
        console.error('Fallback database initialization failed:', fallbackError);
      }
    }
  }

  private async createTables() {
    if (!this.db) return;

    const createTableQuery = `
      CREATE TABLE IF NOT EXISTS quiz_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_index INTEGER NOT NULL,
        exam TEXT NOT NULL,
        selected_answer TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        is_correct BOOLEAN NOT NULL,
        timestamp TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        task_statement TEXT NOT NULL
      );
    `;

    try {
      await this.db.execAsync(createTableQuery);
      // Migration: ensure 'exam' column exists in case the table pre-existed without it
      let columns: any[] = [];
      try {
        columns = await this.db.getAllAsync("PRAGMA table_info(quiz_activity)") as any[];
        console.log('PRAGMA table_info result:', columns);
      } catch (pragmaError) {
        console.warn('Error querying table info for migration:', pragmaError);
      }
      const hasExam = columns.some(col => col.name === 'exam');
      if (!hasExam) {
        try {
          await this.db.execAsync("ALTER TABLE quiz_activity ADD COLUMN exam TEXT NOT NULL DEFAULT ''")
          console.log('Added exam column to quiz_activity table');
        } catch (alterError) {
          console.warn('Error adding exam column:', alterError);
        }
      } else {
        console.log('Exam column already exists, skipping migration');
      }
      console.log('Tables created and migrated successfully');
    } catch (error) {
      console.error('Error creating tables:', error);
    }
  }

  async saveQuizActivity(activity: Omit<QuizActivity, 'id'>) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!this.db) {
      console.error('Database not initialized');
      return;
    }

    const insertQuery = `
      INSERT INTO quiz_activity 
      (question_index, exam, selected_answer, correct_answer, is_correct, timestamp, difficulty, task_statement)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    `;

    try {
      await this.db.runAsync(insertQuery, [
        activity.questionIndex,
        activity.exam,  // include exam
        activity.selectedAnswer,
        activity.correctAnswer,
        activity.isCorrect ? 1 : 0,
        activity.timestamp,
        activity.difficulty,
        activity.taskStatement
      ]);
      console.log('Quiz activity saved successfully');
    } catch (error) {
      console.error('Error saving quiz activity:', error);
    }
  }

  async getQuizHistory(examFilter?: string): Promise<QuizActivity[]> {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!this.db) {
      console.error('Database not initialized');
      return [];
    }

    const selectQuery = examFilter
      ? `SELECT * FROM quiz_activity WHERE exam = ? ORDER BY timestamp DESC;`
      : `SELECT * FROM quiz_activity ORDER BY timestamp DESC;`;

    try {
      const result = examFilter
        ? await this.db.getAllAsync(selectQuery, [examFilter])
        : await this.db.getAllAsync(selectQuery);
      return result.map((row: any) => ({
        id: row.id,
        questionIndex: row.question_index,
        exam: row.exam,  // include exam in mapping
        selectedAnswer: row.selected_answer,
        correctAnswer: row.correct_answer,
        isCorrect: row.is_correct === 1,
        timestamp: row.timestamp,
        difficulty: row.difficulty,
        taskStatement: row.task_statement
      }));
    } catch (error) {
      console.error('Error getting quiz history:', error);
      return [];
    }
  }

  async getStats(examFilter?: string) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!this.db) {
      console.error('Database not initialized');
      return { total: 0, correct: 0, percentage: 0 };
    }

    try {
      const totalQuery = examFilter
        ? 'SELECT COUNT(*) as total FROM quiz_activity WHERE exam = ?'
        : 'SELECT COUNT(*) as total FROM quiz_activity';
      const correctQuery = examFilter
        ? 'SELECT COUNT(*) as correct FROM quiz_activity WHERE is_correct = 1 AND exam = ?'
        : 'SELECT COUNT(*) as correct FROM quiz_activity WHERE is_correct = 1';
      
      const totalResult = examFilter
        ? await this.db.getFirstAsync(totalQuery, [examFilter]) as any
        : await this.db.getFirstAsync(totalQuery) as any;
      const correctResult = examFilter
        ? await this.db.getFirstAsync(correctQuery, [examFilter]) as any
        : await this.db.getFirstAsync(correctQuery) as any;

      return {
        total: totalResult?.total || 0,
        correct: correctResult?.correct || 0,
        percentage: totalResult?.total > 0 ? Math.round((correctResult?.correct / totalResult?.total) * 100) : 0
      };
    } catch (error) {
      console.error('Error getting stats:', error);
      return { total: 0, correct: 0, percentage: 0 };
    }
  }

  async clearHistory(examFilter?: string) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!this.db) {
      console.error('Database not initialized');
      return;
    }

    try {
      if (examFilter) {
        await this.db.runAsync('DELETE FROM quiz_activity WHERE exam = ?', [examFilter]);
      } else {
        await this.db.runAsync('DELETE FROM quiz_activity');
      }
      console.log('Quiz history cleared successfully');
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  }
}

export const databaseService = new DatabaseService();
