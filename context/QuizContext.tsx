import React, { createContext, ReactNode, useContext, useReducer } from 'react';
import { QuizSession, UserProgress } from '../types';

interface QuizContextType {
  sessions: QuizSession[];
  userProgress: UserProgress;
  addSession: (session: QuizSession) => void;
  updateProgress: (progress: Partial<UserProgress>) => void;
  getSessionsByExam: (examType: string) => QuizSession[];
  clearSessions: () => void;
}

const QuizContext = createContext<QuizContextType | undefined>(undefined);

type QuizAction = 
  | { type: 'ADD_SESSION'; payload: QuizSession }
  | { type: 'UPDATE_PROGRESS'; payload: Partial<UserProgress> }
  | { type: 'CLEAR_SESSIONS' };

interface QuizState {
  sessions: QuizSession[];
  userProgress: UserProgress;
}

const initialState: QuizState = {
  sessions: [],
  userProgress: { 
    totalQuestions: 0, 
    correctAnswers: 0, 
    streakCount: 0, 
    weakTopics: [], 
    strongTopics: [] 
  }
};

const quizReducer = (state: QuizState, action: QuizAction): QuizState => {
  switch (action.type) {
    case 'ADD_SESSION':
      return {
        ...state,
        sessions: [...state.sessions, action.payload]
      };
    case 'UPDATE_PROGRESS':
      return {
        ...state,
        userProgress: { ...state.userProgress, ...action.payload }
      };
    case 'CLEAR_SESSIONS':
      return {
        ...state,
        sessions: []
      };
    default:
      return state;
  }
};

export const QuizProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(quizReducer, initialState);

  const addSession = (session: QuizSession) => {
    dispatch({ type: 'ADD_SESSION', payload: session });
  };

  const updateProgress = (progress: Partial<UserProgress>) => {
    dispatch({ type: 'UPDATE_PROGRESS', payload: progress });
  };

  const clearSessions = () => {
    dispatch({ type: 'CLEAR_SESSIONS' });
  };

  const getSessionsByExam = (examType: string): QuizSession[] => {
    return state.sessions.filter(session => session.examType === examType);
  };

  const value: QuizContextType = {
    sessions: state.sessions,
    userProgress: state.userProgress,
    addSession,
    updateProgress,
    getSessionsByExam,
    clearSessions
  };

  return (
    <QuizContext.Provider value={value}>
      {children}
    </QuizContext.Provider>
  );
};

export const useQuizContext = (): QuizContextType => {
  const context = useContext(QuizContext);
  if (!context) {
    throw new Error('useQuizContext must be used within a QuizProvider');
  }
  return context;
};
