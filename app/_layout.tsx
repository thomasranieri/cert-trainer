import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Select Exam' }} />
      <Stack.Screen name="quiz" options={{ headerShown: false }} />
      <Stack.Screen name="stats" options={{ headerShown: false }} />
      <Stack.Screen name="setup/index" options={{ headerShown: false }} />
    </Stack>
  );
}
