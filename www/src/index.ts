import './src/patch-console-log';
import { initApp } from './src/app';

async function main (): Promise<void> {
  try {
    await initApp();
  } catch (error) {
    console.error('Error initializing the application', error);
  }
}

main();
