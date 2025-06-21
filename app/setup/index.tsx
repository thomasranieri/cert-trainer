import { useState } from 'react';
import { Button, Text, TextInput, View } from 'react-native';
import * as Storage from '../../utils/Storage';

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
        onPress={() => Storage.set("OPENAI_API_KEY", apiKey)} />
    </View>
  );
}
  