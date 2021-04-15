import AsyncStorage from '@react-native-async-storage/async-storage';

const kTrue = 'true';
const kFalse = 'false';

const kKeyFirstLaunch = 'firstAppLaunch';

class LocalStorage {
  /**
   * Whether this is the first app launch
   *
   * @return a promise containing a boolean indicating if it's the first app launch
   */
  async isFirstAppLaunch() {
    try {
      const value = await AsyncStorage.getItem(kKeyFirstLaunch);
      // If not found (null), assumes it's the first app launch
      return value === null || value === kTrue;
    } catch (error) {
      console.error(error);
      return true;
    }
  }

  /**
   * Remember that it's no longer the first app launch
   *
   * @return a promise indicating if the the operation is successful
   */
  unsetFirstAppLaunch() {
    return AsyncStorage.setItem(kKeyFirstLaunch, kFalse);
  }
}

export default new LocalStorage();
