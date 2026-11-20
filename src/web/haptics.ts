// An iOS wrapper can register this WKScriptMessageHandler before loading the game.
type HapticsWindow = Window & {
  webkit?: { messageHandlers?: { makeSomethingHaptics?: {
    postMessage(message: { type: 'combination' }): void;
  } } };
};

export function combinationHaptic() {
  try {
    const native = (window as HapticsWindow).webkit?.messageHandlers?.makeSomethingHaptics;
    if (native) {
      native.postMessage({ type: 'combination' });
      return;
    }
  } catch { /* Fall back if the native bridge is unavailable. */ }
  try { navigator.vibrate?.(20); }
  catch { /* Haptics are optional and must not interrupt play. */ }
}
