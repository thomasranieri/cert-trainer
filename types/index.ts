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

export interface QuizSession {
  id: string;
  examType: string;
  score: number;
  totalQuestions: number;
  timeSpent: number;
  completedAt: Date;
  answers: Record<number, string>;
}

export interface UserProgress {
  totalQuestions: number;
  correctAnswers: number;
  streakCount: number;
  weakTopics: string[];
  strongTopics: string[];
}

export interface QuizStats {
  total: number;
  correct: number;
  percentage: number;
}

export interface DifficultyStats {
  difficulty: string;
  correct: number;
  total: number;
  percentage: number;
}

export interface TaskStats {
  taskStatement: string;
  correct: number;
  total: number;
  percentage: number;
}

export type Difficulty = 'EASY' | 'MEDIUM' | 'HARD';
export type ExamType = 'AIF-C01' | 'SAA-C03' | 'DVA-C01' | string;
export type QuestionType = 'all' | 'unseen';
