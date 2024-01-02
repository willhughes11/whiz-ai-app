import React from "react";
import { View } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import {
  createBottomTabNavigator,
  BottomTabNavigationOptions,
} from "@react-navigation/bottom-tabs";
import Chat from "./Chat";
import ChatPdf from "./ChatPdf";
import BibleGpt from "./BibleGpt";

const Tab = createBottomTabNavigator();
const screenOptions: BottomTabNavigationOptions = {
  tabBarShowLabel: false,
  headerShown: false,
  tabBarStyle: {
    position: "absolute",
    bottom: 0,
    right: 0,
    left: 0,
    elevation: 0,
    height: 60,
    backgroundColor: "#7761ff",
    marginHorizontal: 10,
    marginBottom: 20,
    borderRadius: 9999,
  },
};

export const BottomNavigation = () => {
  return (
    <Tab.Navigator screenOptions={screenOptions}>
      <Tab.Screen
        name="Chat"
        component={Chat}
        options={{
          tabBarIcon: ({ focused }) => {
            return (
              <View
                style={{
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: focused ? "#fff" : "transparent",
                  borderRadius: 9999,
                  width: 40,
                  height: 40,
                }}
              >
                <Ionicons
                  name="chatbox-ellipses-outline"
                  size={30}
                  color={focused ? "#7761ff" : "#fff"}
                  style={{
                    margin: "auto",
                  }}
                />
              </View>
            );
          },
        }}
      />
      <Tab.Screen
        name="ChatPDF"
        component={ChatPdf}
        options={{
          tabBarIcon: ({ focused }) => {
            return (
              <View
                style={{
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: focused ? "#fff" : "transparent",
                  borderRadius: 9999,
                  width: 40,
                  height: 40,
                  padding: "auto",
                }}
              >
                <Ionicons
                  name="document-text-outline"
                  size={30}
                  color={focused ? "#7761ff" : "#fff"}
                  style={{
                    margin: "auto",
                  }}
                />
              </View>
            );
          },
        }}
      />
      <Tab.Screen
        name="BibleGPT"
        component={BibleGpt}
        options={{
          tabBarIcon: ({ focused }) => {
            return (
              <View
                style={{
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: focused ? "#fff" : "transparent",
                  borderRadius: 9999,
                  width: 40,
                  height: 40,
                  padding: "auto",
                }}
              >
                <Ionicons
                  name="book-outline"
                  size={30}
                  color={focused ? "#7761ff" : "#fff"}
                  style={{
                    margin: "auto",
                  }}
                />
              </View>
            );
          },
        }}
      />
    </Tab.Navigator>
  );
};
