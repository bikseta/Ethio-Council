import { createContext, useContext } from 'react';

export interface AuthState {
  token: string | null;
  userId: string | null;
  userRole: string | null;
  fullName: string | null;
  isAuthenticated: boolean;
}

export interface AppStore {
  auth: AuthState;
  setAuth: (auth: Partial<AuthState>) => void;
  logout: () => void;
}

export const StoreContext = createContext<AppStore>({
  auth: {
    token: localStorage.getItem('access_token'),
    userId: localStorage.getItem('user_id'),
    userRole: localStorage.getItem('user_role'),
    fullName: localStorage.getItem('full_name'),
    isAuthenticated: !!localStorage.getItem('access_token'),
  },
  setAuth: () => {},
  logout: () => {},
});

export const useStore = () => useContext(StoreContext);
