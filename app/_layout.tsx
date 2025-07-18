import AntDesign from '@expo/vector-icons/AntDesign';
import { Stack, router } from "expo-router";
import { useEffect } from "react";
import { Pressable, Text } from "react-native";
import { QuizProvider } from "./context/QuizContext";

const HomeButton = () => {

  return (
    <Pressable
      onPress={() => router.push('/')}
      style={{ paddingHorizontal: 16, paddingVertical: 8 }}
    >
      <Text style={{ color: '#007AFF', fontSize: 16 }}>
        <AntDesign name="home" size={16} color="#007AFF" />
      </Text>
    </Pressable>
  );
};

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
            headerLeft: () => null,
          }}
        />
        <Stack.Screen
          name="quiz"
          options={{
            title: "Quiz",
            headerLeft: () => <HomeButton />,
          }}
        />
        <Stack.Screen
          name="stats"
          options={{
            title: "Stats",
            headerLeft: () => <HomeButton />,
          }}
        />
      </Stack>
    </QuizProvider>
  );
}
