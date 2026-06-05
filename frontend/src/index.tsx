/**
 * Refast RefastGrid Extension
 *
 * This extension provides the RefastGrid component.
 *
 * The component is registered with RefastClient's component registry
 * when this script loads after refast-client.js.
 */

import { RefastGrid } from './RefastGrid';

// Type definition for RefastClient
interface RefastClient {
  componentRegistry: {
    register: (name: string, component: React.ComponentType<unknown>) => void;
    has: (name: string) => boolean;
  };
  React: typeof import('react');
  ReactDOM: typeof import('react-dom');
  version: string;
}

declare global {
  interface Window {
    RefastClient?: RefastClient;
  }
}

/**
 * Register the RefastGrid component with Refast.
 *
 * This function is called immediately when the script loads.
 * It checks for RefastClient and registers the component.
 */
function registerComponents(): void {
  if (!window.RefastClient) {
    console.error(
      '[refast-refast_grid] RefastClient not found. ' +
      'Make sure refast-client.js is loaded before this script.'
    );
    return;
  }

  const { componentRegistry } = window.RefastClient;

  // Check if already registered (avoid duplicate registration)
  if (componentRegistry.has('RefastGrid')) {
    console.warn('[refast-refast_grid] RefastGrid already registered, skipping.');
    return;
  }

  // Register the component
  componentRegistry.register('RefastGrid', RefastGrid as React.ComponentType<unknown>);
  console.log('[refast-refast_grid] Registered RefastGrid component');
}

// Register components immediately
registerComponents();

// Export for direct imports (if bundled differently)
export { RefastGrid };
