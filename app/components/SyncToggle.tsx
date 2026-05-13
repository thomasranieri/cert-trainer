import React, { useEffect, useState } from "react";
import {
    ActivityIndicator,
    Alert,
    StyleSheet,
    Text,
    TextInput,
    TouchableOpacity,
    View,
} from "react-native";
import {
    getCurrentUser,
    isFirebaseConfigured,
    signInWithEmail,
    signOutCurrentUser,
    signUpWithEmail,
    subscribeToAuthState,
} from "../services/firebase.config";

export const SyncToggle: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);

  useEffect(() => {
    let unsubscribe: (() => void) | undefined;

    const init = async () => {
      if (!isFirebaseConfigured()) {
        setIsLoading(false);
        return;
      }

      try {
        unsubscribe = await subscribeToAuthState((user) => {
          setUserEmail(user?.email || null);
          setIsLoading(false);
        });

        const currentUser = getCurrentUser();
        setUserEmail(currentUser?.email || null);
      } catch (error) {
        console.error("Failed to initialize account state:", error);
        setIsLoading(false);
      }
    };

    init();

    return () => {
      unsubscribe?.();
    };
  }, []);

  const validateInputs = () => {
    if (!email.trim()) {
      Alert.alert("Email required", "Enter your email address to continue.");
      return false;
    }

    if (password.length < 6) {
      Alert.alert("Password too short", "Use at least 6 characters.");
      return false;
    }

    return true;
  };

  const handleSignIn = async () => {
    if (!validateInputs()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await signInWithEmail(email.trim(), password);
      setPassword("");
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Sign in failed.";
      Alert.alert("Unable to sign in", message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSignUp = async () => {
    if (!validateInputs()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await signUpWithEmail(email.trim(), password);
      setPassword("");
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Sign up failed.";
      Alert.alert("Unable to create account", message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSignOut = async () => {
    setIsSubmitting(true);
    try {
      await signOutCurrentUser();
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Sign out failed.";
      Alert.alert("Unable to sign out", message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <View style={styles.container}>
        <View style={styles.loadingRow}>
          <ActivityIndicator size="small" color="#1976D2" />
          <Text style={styles.label}>Loading account...</Text>
        </View>
      </View>
    );
  }

  if (!isFirebaseConfigured()) {
    return (
      <View style={styles.container}>
        <Text style={styles.label}>Cloud sync unavailable</Text>
        <Text style={styles.description}>Firebase env vars are missing.</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Cloud Account</Text>
      {userEmail ? (
        <>
          <Text style={styles.description}>Signed in as {userEmail}</Text>
          <TouchableOpacity
            style={[
              styles.button,
              styles.signOutButton,
              isSubmitting && styles.buttonDisabled,
            ]}
            onPress={handleSignOut}
            disabled={isSubmitting}
          >
            <Text style={styles.buttonText}>Sign Out</Text>
          </TouchableOpacity>
        </>
      ) : (
        <>
          <Text style={styles.description}>
            Sign in to sync progress across devices.
          </Text>
          <TextInput
            style={styles.input}
            placeholder="Email"
            autoCapitalize="none"
            keyboardType="email-address"
            value={email}
            onChangeText={setEmail}
          />
          <TextInput
            style={styles.input}
            placeholder="Password"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
          />
          <View style={styles.buttonRow}>
            <TouchableOpacity
              style={[styles.button, isSubmitting && styles.buttonDisabled]}
              onPress={handleSignIn}
              disabled={isSubmitting}
            >
              <Text style={styles.buttonText}>Sign In</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.button,
                styles.secondaryButton,
                isSubmitting && styles.buttonDisabled,
              ]}
              onPress={handleSignUp}
              disabled={isSubmitting}
            >
              <Text style={styles.buttonText}>Sign Up</Text>
            </TouchableOpacity>
          </View>
        </>
      )}
      {isSubmitting && (
        <View style={styles.loadingRow}>
          <ActivityIndicator size="small" color="#1976D2" />
          <Text style={styles.description}>Processing...</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#e5e5e5",
  },
  loadingRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  label: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 4,
  },
  description: {
    fontSize: 13,
    color: "#666",
    marginBottom: 8,
  },
  input: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#d7d7d7",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 10,
    marginBottom: 8,
  },
  buttonRow: {
    flexDirection: "row",
    gap: 8,
  },
  button: {
    flex: 1,
    backgroundColor: "#1976D2",
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
  },
  secondaryButton: {
    backgroundColor: "#2E7D32",
  },
  signOutButton: {
    width: "100%",
    backgroundColor: "#424242",
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: "white",
    fontWeight: "600",
  },
});
