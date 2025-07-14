import AntDesign from '@expo/vector-icons/AntDesign';
import { Link } from 'expo-router';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

interface SocialFooterProps {
  isNarrowScreen: boolean;
}

const SocialFooter: React.FC<SocialFooterProps> = ({ isNarrowScreen }) => {
  return (
    <View style={styles.getInTouch}>
      <Link href="https://www.linkedin.com/in/thomas-ranieri-dev/" style={styles.socialLink} target='_blank'>
        <AntDesign name="linkedin-square" size={24} color="white" />
        {!isNarrowScreen && <Text style={styles.getInTouchText}>thomas-ranieri-dev</Text>}
      </Link>
      <Link href="https://github.com/thomasranieri/cert-trainer" style={styles.socialLink} target='_blank'>
        <AntDesign name="github" size={24} color="white" />
        {!isNarrowScreen && <Text style={styles.getInTouchText}>thomasranieri/cert-trainer</Text>}
      </Link>
      <Link href="mailto:tom@classgen.com" style={styles.socialLink} target='_blank'>
        <AntDesign name="mail" size={24} color="white" />
        {!isNarrowScreen && <Text style={styles.getInTouchText}>tom@classgen.com</Text>}
      </Link>
    </View>
  );
};

const styles = StyleSheet.create({
  getInTouch: {
    marginTop: 20,
    backgroundColor: '#5252bb',
    flexDirection: 'row',
    display: 'flex',
    justifyContent: 'space-around',
  },
  socialLink: {
    justifyContent: 'center',
    alignItems: 'center',
    display: 'flex',
    padding: 10,
  },
  getInTouchText: {
    color: 'white',
    fontSize: 16,
    marginLeft: 8,
  },
});

export default SocialFooter;
