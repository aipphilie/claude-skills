import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {Sheet} from './Sheet';
import {Variants} from './Variants';
import {Riders} from './Riders';
import {KristinaSheet} from './KristinaSheet';
import {Storyboard} from './boards/Storyboard';
import {timeline} from './lib';
export const Root: React.FC = () => (
  <>
  <Composition id="Storyboard" component={Storyboard} width={2420} height={3050} fps={30} durationInFrames={1} />
  <Composition id="KristinaSheet" component={KristinaSheet} width={1760} height={1400} fps={30} durationInFrames={1} />
  <Composition id="Riders" component={Riders} width={2460} height={1420} fps={30} durationInFrames={1} />
  <Composition id="Variants" component={Variants} width={2500} height={1200} fps={30} durationInFrames={1} />
  <Composition id="Sheet" component={Sheet} width={2400} height={960} fps={30} durationInFrames={1} />
  <Composition id="Ashot" component={Video} width={1080} height={1920} fps={30} durationInFrames={timeline.frames} />
  </>
);
