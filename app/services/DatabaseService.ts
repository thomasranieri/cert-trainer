import { get, ref, set } from "firebase/database";
import {
  getCurrentUser,
  getFirebaseDb,
  initializeFirebase,
} from "./firebase.config";

export interface Question {
  id?: string;
  taskStatement: string;
  exam?: string;
  stem: string;
  correct: string;
  difficulty: "EASY" | "MEDIUM" | "HARD";
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

class DatabaseService {
  private key = "quizHistory";
  private userId: string = "";

  async initialize() {
    try {
      await initializeFirebase();
      const user = getCurrentUser();
      this.userId = user?.uid || "";
    } catch (error) {
      console.error("Failed to initialize Firebase:", error);
    }
  }

  private async requireUserId(): Promise<string | null> {
    await this.initialize();
    if (this.userId) {
      return this.userId;
    }

    const user = getCurrentUser();
    if (user?.uid) {
      this.userId = user.uid;
      return this.userId;
    }

    return null;
  }

  async setSyncEnabled(_: boolean) {
    return;
  }

  async isSyncEnabled(): Promise<boolean> {
    return true;
  }

  private async writeHistory(list: QuizActivity[]) {
    const userId = await this.requireUserId();
    if (!userId) {
      throw new Error("You must sign in to sync quiz history.");
    }

    try {
      const db = getFirebaseDb();
      if (!db) {
        throw new Error("Firebase Realtime Database is not initialized.");
      }

      await set(ref(db, `users/${userId}/${this.key}`), list);
    } catch (error) {
      console.error("Firebase write failed:", error);
      throw error;
    }
  }

  private async readHistory(): Promise<QuizActivity[]> {
    const userId = await this.requireUserId();
    if (!userId) {
      return [];
    }

    try {
      const db = getFirebaseDb();
      if (!db) return [];

      const snapshot = await get(ref(db, `users/${userId}/${this.key}`));
      if (snapshot.exists()) {
        return snapshot.val() || [];
      }
    } catch (error) {
      console.error("Firebase fetch failed:", error);
    }
    return [];
  }

  async saveQuizActivity(activity: QuizActivity) {
    const list = await this.readHistory();
    list.unshift(activity);
    await this.writeHistory(list);

    return;
  }

  async getQuizHistory(examFilter?: string): Promise<QuizActivity[]> {
    let list = await this.readHistory();

    if (examFilter) {
      list = list.filter((q) => q.exam === examFilter);
    }
    return list;
  }

  async getStats(examFilter?: string) {
    let list = await this.readHistory();

    if (examFilter) {
      list = list.filter((q) => q.exam === examFilter);
    }
    const total = list.length;
    const correct = list.filter((q) => q.isCorrect).length;
    return {
      total,
      correct,
      percentage: total ? Math.round((correct / total) * 100) : 0,
    };
  }

  async clearHistory(examFilter?: string) {
    const userId = await this.requireUserId();
    if (!userId) {
      return;
    }

    const list = await this.readHistory();

    if (examFilter) {
      const filtered = list.filter((q) => q.exam !== examFilter);
      await this.writeHistory(filtered);
    } else {
      await this.writeHistory([]);
    }

    return;
  }
}

export const databaseService = new DatabaseService();
