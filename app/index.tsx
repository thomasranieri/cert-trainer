import { Link } from "expo-router";
import OpenAI from "openai";
import { useState } from "react";
import { Button, Text, View } from "react-native";
import * as Storage from "./utils/Storage";


export default function Index() {
  let [output, setOutput] = useState("");
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>cert-trainer</Text>
      <Link href="/setup">
        Go to Setup
      </Link>
      <Text>
        {output ? `Output: ${output}` : "No output generated yet."}
      </Text>
      <Button
        title="Generate Output"
        onPress={async () => {
          console.log("Generating output...");
          var apiKey = await Storage.get("OPENAI_API_KEY");
          if (!apiKey) {
            console.error("API key not found. Please set it up first.");
            return;
          }
          const client = new OpenAI({
            apiKey: apiKey,
            dangerouslyAllowBrowser: true
          });

          const response = await client.responses.create({
            model: 'gpt-4o',
            instructions: 'You are a coding assistant that talks like a pirate',
            input: 'Are semicolons optional in JavaScript?',
          });

          setOutput(response.output_text);
        }}
      />
    </View>
  );
}
