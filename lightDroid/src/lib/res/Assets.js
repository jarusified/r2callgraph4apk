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
    case 'tertiary':
      return '#ffbf01'; // UC Davis's Yellow Color (#pane-content). See #pane-content of https://www.ucdavis.edu/
    case 'dark-tertiary':
      return '#ed8b00'; // UC Davis's Orange Color (#pane-content). See #pane-content of https://www.ucdavis.edu/
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
