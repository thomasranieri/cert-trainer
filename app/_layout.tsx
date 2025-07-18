import { Stack } from "expo-router";
import { useEffect } from "react";
import { QuizProvider } from "./context/QuizContext";

export default function RootLayout() {
  useEffect(() => {
    console.log(`Version: ${process.env.EXPO_PUBLIC_BUILD_DATE} ${process.env.EXPO_PUBLIC_COMMIT_HASH?.slice(0, 7)}`);
  }, []);
  return (
    <QuizProvider>
      <Stack>
        <Stack.Screen
          name="index"
          options={{
            title: "Cert Trainer",
          }}
        />
        <Stack.Screen
          name="quiz"
          options={{
            title: "Quiz",
          }}
        />
        <Stack.Screen
          name="stats"
          options={{
            title: "Stats",
          }}
        />
      </Stack>
    </QuizProvider>
  );
}
