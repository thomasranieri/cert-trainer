import { Button, Text, TextInput, View } from 'react-native';

import * as SecureStore from 'expo-secure-store';
import { useState } from 'react';

async function save(key: string, value: string) {
    await SecureStore.setItemAsync(key, value);
}

export default function Setup() {
  let [apiKey, setApiKey] = useState("");
  return (
    <View>
      <Text>Setup Screen</Text>
      <TextInput
        placeholder="Enter your OpenAI API Key"
        value={apiKey}
        onChangeText={setApiKey}
      />
      <Button
      title="Save API Key"
       onPress={() => save("OPENAI_API_KEY", apiKey)} />
    </View>
  );
}
