import { initializeApp } from "firebase/app";
import {
    Auth,
    User,
    createUserWithEmailAndPassword,
    getAuth,
    onAuthStateChanged,
    signInWithEmailAndPassword,
    signOut,
} from "firebase/auth";
import { getDatabase } from "firebase/database";

// Replace with your Firebase config from Firebase Console
// https://firebase.google.com/docs/web/setup#web-setup
const firebaseConfig = {
  apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY || "",
  authDomain: process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN || "",
  projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID || "",
  storageBucket: process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET || "",
  messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "",
  appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID || "",
  databaseURL: process.env.EXPO_PUBLIC_FIREBASE_DATABASE_URL || "",
};

let app: any;
let db: any;
let auth: Auth;
let currentUser: User | null = null;
let isInitialized = false;
let hasAuthListener = false;

export const initializeFirebase = async () => {
  if (isInitialized || !firebaseConfig.apiKey) return;

  app = initializeApp(firebaseConfig);
  db = getDatabase(app);
  auth = getAuth(app);

  if (!hasAuthListener) {
    onAuthStateChanged(auth, (user) => {
      currentUser = user;
    });
    hasAuthListener = true;
  }

  currentUser = auth.currentUser;
  isInitialized = true;
};

const requireAuth = async () => {
  await initializeFirebase();
  if (!auth) {
    throw new Error("Firebase Auth is not initialized.");
  }
};

export const signUpWithEmail = async (email: string, password: string) => {
  await requireAuth();
  const userCred = await createUserWithEmailAndPassword(auth, email, password);
  currentUser = userCred.user;
  return userCred.user;
};

export const signInWithEmail = async (email: string, password: string) => {
  await requireAuth();
  const userCred = await signInWithEmailAndPassword(auth, email, password);
  currentUser = userCred.user;
  return userCred.user;
};

export const signOutCurrentUser = async () => {
  await requireAuth();
  await signOut(auth);
  currentUser = null;
};

export const subscribeToAuthState = async (
  callback: (user: User | null) => void,
) => {
  await initializeFirebase();
  if (!auth) {
    callback(null);
    return () => undefined;
  }

  return onAuthStateChanged(auth, callback);
};

export const getFirebaseDb = () => db;
export const getFirebaseAuth = () => auth;
export const getCurrentUser = () => currentUser;
export const isFirebaseConfigured = () => !!firebaseConfig.apiKey;
export const isAuthenticated = () => !!currentUser;
