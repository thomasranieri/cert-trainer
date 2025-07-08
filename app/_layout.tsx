import { Stack } from "expo-router";
import { StatusBar } from "react-native";


export default function RootLayout() {
  return (
    <>
      <Stack>
        <Stack.Screen name="index" options={{ title: 'Select Exam' }} />
        <Stack.Screen name="quiz" options={{ headerShown: false }} />
        <Stack.Screen name="stats" options={{ headerShown: false }} />
      </Stack>
      <StatusBar barStyle="dark-content" />
    </>
  );
}
