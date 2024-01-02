import { StyleSheet, Text, View, Dimensions } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import Chat from "./src/components/Chat";
import { createDrawerNavigator, DrawerNavigationOptions } from "@react-navigation/drawer";
import ChatPdf from "./src/components/ChatPdf";
import BibleGpt from "./src/components/BibleGpt";
import { BottomNavigation } from "./src/components/BottomNavigation";

const Drawer = createDrawerNavigator();
const screenOptions: DrawerNavigationOptions = {
};

const { width, height } = Dimensions.get("window");

export default function App() {
  const thresholdWidth = 500;

  return (
    <NavigationContainer>
      {width > thresholdWidth ? <DrawerNavigation /> : <BottomNavigation />}
    </NavigationContainer>
  );
}

const DrawerNavigation = () => {
  return (
    <Drawer.Navigator>
      <Drawer.Screen name="Chat" component={Chat} />
      <Drawer.Screen name="ChatPDF" component={ChatPdf} />
      <Drawer.Screen name="BibleGPT" component={BibleGpt} />
    </Drawer.Navigator>
  );
};
