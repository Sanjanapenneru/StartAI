import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import {
  GoogleAuthProvider,
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
  updateProfile,
} from "firebase/auth";
import { auth, firebaseReady } from "../services/firebase";

const AuthContext = createContext(null);
const googleProvider = new GoogleAuthProvider();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!firebaseReady || !auth) {
      setLoading(false);
      return undefined;
    }
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  const requireAuth = () => {
    if (!auth) {
      throw new Error("Authentication is not configured for this environment.");
    }
    return auth;
  };

  const signup = async (email, password, displayName) => {
    const result = await createUserWithEmailAndPassword(
      requireAuth(),
      email,
      password
    );
    if (displayName) await updateProfile(result.user, { displayName });
    return result;
  };

  const login = (email, password) =>
    signInWithEmailAndPassword(requireAuth(), email, password);
  const googleLogin = () => signInWithPopup(requireAuth(), googleProvider);
  const logout = () => signOut(requireAuth());
  const getToken = async () => (user ? user.getIdToken() : null);

  return (
    <AuthContext.Provider
      value={{ user, loading, signup, login, googleLogin, logout, getToken }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}