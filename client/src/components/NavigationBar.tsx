import React from "react";
import { Text, View, StyleSheet, Button } from "react-native";

const NavigationBar = () => {
  return (
    <View style={styles.container} className="bg-violet-600">
      <Text className="text-white">Chat</Text>
      <Text className="text-white">ChatPDF</Text>
      <Text className="text-white">BibleGPT</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    padding: 10,
    margin: 10,
    borderRadius: 20
  },
});

export default NavigationBar;
