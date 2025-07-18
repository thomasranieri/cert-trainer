import { Stack } from "expo-router";
import { QuizProvider } from "./context/QuizContext";

export default function RootLayout() {
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
