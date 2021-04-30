import {StyleSheet} from 'react-native';

function getColor(name) {
  switch (name) {
    case 'theme':
      return 'rgb(144, 178, 185)';
    case 'primary':
      return '#000';
    case 'light-primary':
      return '#ccc';
    case 'secondary':
      return '#023858';
    case 'malicious':
      return '#D90263';
    case 'benign':
      return '#0952CE';
    case 'background':
      return '#fff';
    case 'dark-background':
      return '#eee';
    case 'surface':
      return '#aaa';
    case 'dark-surface':
      return '#666';
    default:
      return '#f00'; // Making it red can easily detect the problem.
  }
}

const AppStyles = StyleSheet.create({
  layout: {
    flex: 1,
    alignItems: 'center',
    backgroundColor: getColor('background'),
  },
});

export {AppStyles, getColor};
