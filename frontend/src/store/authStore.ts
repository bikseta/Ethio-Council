export type AuthUser = {
  token: string | null;
  email: string | null;
  fullName: string | null;
};

const KEY = 'ecfe_auth';

export const authStore = {
  get(): AuthUser {
    const raw = localStorage.getItem(KEY);
    if (!raw) {
      return { token: null, email: null, fullName: null };
    }
    return JSON.parse(raw) as AuthUser;
  },
  set(user: AuthUser) {
    if (user.token) {
      localStorage.setItem('ecfe_token', user.token);
    } else {
      localStorage.removeItem('ecfe_token');
    }
    localStorage.setItem(KEY, JSON.stringify(user));
  },
  clear() {
    localStorage.removeItem(KEY);
    localStorage.removeItem('ecfe_token');
  },
};
