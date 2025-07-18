import { useEffect, useState } from 'react';
import { useWindowDimensions } from 'react-native';

/**
 * A custom hook that safely handles window dimensions to avoid hydration mismatches.
 * Returns null during SSR/initial render and actual dimensions after hydration.
 */
export const useClientDimensions = () => {
  const { width, height } = useWindowDimensions();
  const [clientDimensions, setClientDimensions] = useState<{
    width: number | null;
    height: number | null;
  }>({
    width: null,
    height: null,
  });
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    // Set dimensions only after component has mounted (client-side)
    setClientDimensions({ width, height });
    setIsHydrated(true);
  }, [width, height]);

  return { ...clientDimensions, isHydrated };
};
