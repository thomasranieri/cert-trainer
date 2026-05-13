import { useEffect, useState } from "react";
import { databaseService } from "../services/DatabaseService";
import { isFirebaseConfigured } from "../services/firebase.config";

export const useSyncSettings = () => {
  const [syncEnabled, setSyncEnabledState] = useState<boolean>(false);
  const [isAvailable, setIsAvailable] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const initSync = async () => {
      setIsAvailable(isFirebaseConfigured());
      const enabled = await databaseService.isSyncEnabled();
      setSyncEnabledState(enabled);
      setIsLoading(false);
    };
    initSync();
  }, []);

  const toggleSync = async (enabled: boolean) => {
    await databaseService.setSyncEnabled(enabled);
    setSyncEnabledState(enabled);
  };

  return { syncEnabled, isAvailable, isLoading, toggleSync };
};
