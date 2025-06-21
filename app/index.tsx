import { Link } from "expo-router";
import { Text, View } from "react-native";

export default function Index() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>cert-trainer</Text>
      <Link href="/setup/">
        <Text style={{ color: "blue" }}>Go to Setup</Text>
      </Link>
    </View>
  );
}
