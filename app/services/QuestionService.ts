import { Difficulty, ExamType, Question } from '../types';

export class QuestionService {
  private questions: Question[] = [];

  constructor(questions: Question[]) {
    this.questions = questions;
  }

  getQuestionsByExam(examType: ExamType): Question[] {
    return this.questions.filter(q => q.exam === examType);
  }

  getQuestionsByDifficulty(difficulty: Difficulty): Question[] {
    return this.questions.filter(q => q.difficulty === difficulty);
  }

  getQuestionsByTask(taskStatement: string): Question[] {
    return this.questions.filter(q => q.taskStatement === taskStatement);
  }

  getRandomQuestions(count: number, examType?: ExamType): Question[] {
    let pool = examType ? this.getQuestionsByExam(examType) : this.questions;
    
    if (pool.length <= count) return pool;
    
    const shuffled = this.shuffleQuestions([...pool]);
    return shuffled.slice(0, count);
  }

  shuffleQuestions<T>(array: T[]): T[] {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }

  searchQuestions(query: string): Question[] {
    const lowercaseQuery = query.toLowerCase();
    return this.questions.filter(q => 
      q.stem.toLowerCase().includes(lowercaseQuery) ||
      q.taskStatement.toLowerCase().includes(lowercaseQuery)
    );
  }

  getQuestionStats(examType?: ExamType): {
    total: number;
    byDifficulty: Record<Difficulty, number>;
    byTask: Record<string, number>;
  } {
    const pool = examType ? this.getQuestionsByExam(examType) : this.questions;
    
    return {
      total: pool.length,
      byDifficulty: pool.reduce((acc, q) => {
        acc[q.difficulty] = (acc[q.difficulty] || 0) + 1;
        return acc;
      }, {} as Record<Difficulty, number>),
      byTask: pool.reduce((acc, q) => {
        acc[q.taskStatement] = (acc[q.taskStatement] || 0) + 1;
        return acc;
      }, {} as Record<string, number>)
    };
  }

  getAvailableTaskStatements(examType?: ExamType): string[] {
    const pool = examType ? this.getQuestionsByExam(examType) : this.questions;
    return [...new Set(pool.map(q => q.taskStatement))].sort();
  }

  getDifficultyColor(difficulty: string): string {
    switch (difficulty) {
      case 'EASY':
        return '#4CAF50';
      case 'MEDIUM':
        return '#FF9800';
      case 'HARD':
        return '#F44336';
      default:
        return '#757575';
    }
  }

  validateAnswer(selectedAnswer: string, correctAnswer: string): boolean {
    return selectedAnswer === correctAnswer;
  }
}
