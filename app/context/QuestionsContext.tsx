import React, { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react';
import defaultQuestionsData from '../data/questions.json';
import { Question } from '../types';

type QuestionSource = 'local' | 'remote';

interface QuestionsContextValue {
  questions: Question[];
  loading: boolean;
  error: string | null;
  source: QuestionSource;
  requestedUrl: string | null;
  resolvedUrl: string | null;
}

interface QuestionsProviderProps {
  children: ReactNode;
  questionsUrl?: string | null;
}

const QuestionsContext = createContext<QuestionsContextValue | undefined>(undefined);

const defaultQuestions = defaultQuestionsData as Question[];

const normalizeUrl = (value: string): string => {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
};

export const QuestionsProvider: React.FC<QuestionsProviderProps> = ({ children, questionsUrl }) => {
  const [questions, setQuestions] = useState<Question[]>(defaultQuestions);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [source, setSource] = useState<QuestionSource>('local');
  const [resolvedUrl, setResolvedUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!questionsUrl) {
      setQuestions(defaultQuestions);
      setSource('local');
      setResolvedUrl(null);
      setError(null);
      setLoading(false);
      return;
    }

    const normalizedUrl = normalizeUrl(questionsUrl);
    let remoteUrl: URL;

    try {
      remoteUrl = new URL(normalizedUrl);
      if (!['http:', 'https:'].includes(remoteUrl.protocol)) {
        throw new Error('Only http and https URLs are supported.');
      }
    } catch (err) {
      console.error('Invalid questions URL:', err);
      setError('Invalid questions URL');
      setQuestions(defaultQuestions);
      setSource('local');
      setResolvedUrl(null);
      setLoading(false);
      return;
    }

    let isActive = true;
    setLoading(true);
    setError(null);
    setResolvedUrl(null);
    setQuestions([]);

    fetch(remoteUrl.toString())
      .then(async response => {
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }
        const data = await response.json();
        if (!Array.isArray(data)) {
          throw new Error('Expected an array of questions');
        }
        if (!isActive) {
          return;
        }
        setQuestions(data as Question[]);
        setSource('remote');
        setResolvedUrl(remoteUrl.toString());
      })
      .catch(err => {
        if (!isActive) {
          return;
        }
        console.error('Failed to load remote questions:', err);
        setError(err instanceof Error ? err.message : 'Failed to load remote questions');
        setQuestions(defaultQuestions);
        setSource('local');
        setResolvedUrl(null);
      })
      .finally(() => {
        if (!isActive) {
          return;
        }
        setLoading(false);
      });

    return () => {
      isActive = false;
    };
  }, [questionsUrl]);

  const normalizedRequestedUrl = useMemo(() => {
    if (!questionsUrl) {
      return null;
    }
    return normalizeUrl(questionsUrl);
  }, [questionsUrl]);

  const value = useMemo<QuestionsContextValue>(() => ({
    questions,
    loading,
    error,
    source,
    requestedUrl: normalizedRequestedUrl,
    resolvedUrl,
  }), [questions, loading, error, source, normalizedRequestedUrl, resolvedUrl]);

  return (
    <QuestionsContext.Provider value={value}>
      {children}
    </QuestionsContext.Provider>
  );
};

export const useQuestions = (): QuestionsContextValue => {
  const context = useContext(QuestionsContext);
  if (!context) {
    throw new Error('useQuestions must be used within a QuestionsProvider');
  }
  return context;
};
