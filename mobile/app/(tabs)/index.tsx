import { WebView } from 'react-native-webview';
import { View } from 'react-native';

export default function Index() {
  return (
    <View style={{ flex: 1 }}>
      <WebView
        source={{ uri: "http://192.168.1.3:3000" }}
        style={{ flex: 1 }}
      />
    </View>
  );
}
