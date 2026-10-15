/* The effects m360 OS ships, as the real packages from Libraries.dev and React Bits, bundled once
   into window.FX so the single page can use them without a module system. React comes from the page
   (see shims/), so every component shares the one React the app runs on. Build: ./build.sh */
import {ThinkingOrb} from 'thinking-orbs';
import {BorderBeam} from 'border-beam';
import {VoiceBeam, useMicrophone} from 'voice-glow';
import {BotAvatar} from 'bot-avatars';

/* metal-fx is retired (v36.2): its chromatic text and buttons drew coloured ghost copies of numbers and words,
   so the page draws them plain and the package is no longer bundled. */
import BellToggle from './BellToggle.jsx';

window.FX = {ThinkingOrb, BorderBeam, VoiceBeam, useMicrophone, BotAvatar, BellToggle,
  version: {orbs: '0.3.2', beam: '1.4.1', voice: '0.2.1', bots: '0.2.1', bell: 'react-bits'}};
