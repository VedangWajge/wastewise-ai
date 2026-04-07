import { WebView } from 'react-native-webview';
import { View } from 'react-native';

export default function Index() {
  return (
    <View style={{ flex: 1 }}>
      <WebView
        source={{ uri: "http://10.228.33.137:3000" }}
        style={{ flex: 1 }}
      />
    </View>
  );
}
