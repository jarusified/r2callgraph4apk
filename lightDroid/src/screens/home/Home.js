import React, {useEffect, useState} from 'react';
import {
  View,
  ScrollView,
  Text,
  StyleSheet,
  TouchableOpacity,
  LayoutAnimation,
  Dimensions,
  Linking,
  FlatList,
} from 'react-native';
import {Icon} from 'react-native-elements';
import ViewMoreText from 'react-native-view-more-text';
import {getColor} from 'lib/res/Assets';
import {AppInstalledChecker} from 'react-native-check-app-install';
import {AnimatedCircularProgress} from 'react-native-circular-progress';

const {height} = Dimensions.get('window');

const styles = StyleSheet.create({
  body: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: '400',
    color: getColor('secondary'),
  },
  checkList: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    height: 56,
    width: Dimensions.get('window').width,
    paddingLeft: 25,
    paddingRight: 18,
    alignItems: 'center',
    backgroundColor: getColor('background'),
    borderWidth: 1,
    borderColor: getColor('light-primary'),
  },
  checkbox: {
    backgroundColor: getColor('background'),
  },
  parentContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    width: '100%',
  },
  contentContainer: {
    backgroundColor: getColor('background'),
    paddingLeft: 20,
    paddingTop: 10,
    width: Dimensions.get('window').width,
    flexDirection: 'column',
    justifyContent: 'space-between',
  },
  viewMoreText: {
    backgroundColor: getColor('background'),
    paddingLeft: 20,
    color: getColor('secondary'),
  },
  content: {
    fontSize: 16,
    fontWeight: '400',
  },
  link: {
    fontSize: 16,
    fontWeight: '400',
    color: getColor('secondary'),
  },
  topCircle: {
    marginBottom: 20,
  },
  text: {
    marginTop: 10,
    alignSelf: 'center',
  },
});

export default function Home({navigation}) {
  const [appList, setAppList] = useState([]);
  const [maliciousApps, setMaliciousApps] = useState(5);
  /**
   * TODO: Fix force re-render when update occurs
   * Calling this causes the all the components in the screen to refresh.
   * This needs to be fixed. It should not re-render the whole screen’s content,
   * but rather only the UI component related to it.
   * Additionally, the UI shakes when we try to check on it.
   */
  const [, _forceUpdateScreen] = React.useState(0);
  const forceUpdateScreen = () => {
    _forceUpdateScreen({});
  }; // used to force rerender

  // Flatlist item.
  function Item({data, rerender}) {
    // Handle on expand interaction on side goal.
    function handleOnExpand(d) {
      LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut); // Enables some animation on the element.
      d.expanded = !d.expanded; // Set if the side goal is expanded or not.
      rerender();
    }

    function renderViewMore(onPress) {
      return (
        <Text style={styles.viewMoreText} onPress={onPress}>
          View more
        </Text>
      );
    }

    function renderViewLess(onPress) {
      return (
        <Text style={styles.viewMoreText} onPress={onPress}>
          View less
        </Text>
      );
    }

    return (
      <View key={data.title}>
        <TouchableOpacity
          style={styles.checkList}
          onPress={() => handleOnExpand(data)}>
          <Text style={styles.title}>{data.title}</Text>
          <Icon
            type="font-awesome"
            name="external-link"
            size={20}
            style={styles.checkbox}
            color={getColor('malicious')}
          />
        </TouchableOpacity>
        <View style={styles.parentContainer} />
        {data.expanded && (
          <ViewMoreText
            numberOfLines={3}
            renderViewMore={renderViewMore}
            renderViewLess={renderViewLess}
            textStyle={styles.contentContainer}>
            <Text style={styles.content}>{data.content}</Text>
            {'\n'}
            <Text
              style={styles.link}
              onPress={() => Linking.openURL(data.link)}>
              {data.link == null ? '' : 'Source'}
            </Text>
          </ViewMoreText>
        )}
      </View>
    );
  }

  const fetchAppList = async () => {
    const apps = AppInstalledChecker.getAppList();
    const data = apps.map(app => {
      return {
        title: app,
        expanded: false,
      };
    });
    setAppList(data);
  };

  useEffect(() => {
    // We refresh the results only when this component is on focus.
    fetchAppList();
  }, []);

  return (
    <ScrollView>
      <View style={styles.body}>
        <AnimatedCircularProgress
          style={styles.topProgressCircle}
          size={height / 4}
          width={20}
          fill={(maliciousApps / appList.length) * 100}
          tintColor={getColor('benign')}
          backgroundColor={getColor('malicious')}>
          {() => (
            <View>
              <Text style={[styles.text]}>
                {maliciousApps + '/' + appList.length + ' Malwares'}
              </Text>
            </View>
          )}
        </AnimatedCircularProgress>
      </View>
      <FlatList
        data={appList}
        renderItem={({item}) => (
          <Item data={item} rerender={forceUpdateScreen} />
        )}
        keyExtractor={(item, index) => index + item}
      />
    </ScrollView>
  );
}
