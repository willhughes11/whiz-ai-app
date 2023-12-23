import { StyleSheet, Text, View, Dimensions } from "react-native";
import NavigationBar from "./src/components/NavigationBar";
import Chat from "./src/components/Chat";

const { width, height } = Dimensions.get('window');

export default function App() {
  return (
    <View style={styles.container}>
      <View style={styles.chatContainer}>
        <Chat />
      </View>
      <View style={styles.navigationBar} className="w-full">
        <NavigationBar />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: "flex",
    backgroundColor: "#fff",
    minHeight: "auto"
  },
  chatContainer: {
    flex: 1
  },
  navigationBar: {
    display: "flex"
  }
});
