import { Stack } from "expo-router";


export default function RootLayout() {
  return (
    <>
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
    </>
  );
}
