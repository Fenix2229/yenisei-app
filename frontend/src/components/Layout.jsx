import { Outlet } from 'react-router-dom';
import { useState } from 'react';
import Navigation from './Navigation';
import WelcomeScreen from './WelcomeScreen';

const Layout = () => {
  const [showWelcome, setShowWelcome] = useState(false);

  const handleWelcomeClose = () => {
    setShowWelcome(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {showWelcome && <WelcomeScreen onClose={handleWelcomeClose} />}
      <Navigation onShowWelcome={() => setShowWelcome(true)} />
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm">
            © 2026 История реки Енисей. Все права защищены.
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Образовательный проект о великой сибирской реке
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;