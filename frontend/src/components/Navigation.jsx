import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Clock, Map, Image, Brain, Waves, Info, X, Menu } from 'lucide-react';

const Navigation = ({ onShowWelcome }) => {
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  const navItems = [
    { path: '/', icon: Home, label: 'Главная' },
    { path: '/timeline', icon: Clock, label: 'Лента времени' },
    { path: '/map', icon: Map, label: 'Карта' },
    { path: '/gallery', icon: Image, label: 'Галерея' },
    { path: '/quiz', icon: Brain, label: 'Викторина' },
  ];

  const handleNavClick = () => {
    setIsMenuOpen(false);
  };

  const handleShowWelcome = () => {
    setIsMenuOpen(false);
    onShowWelcome();
  };
  
  return (
    <nav className="bg-white shadow-lg relative">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Логотип */}
          <Link to="/" className="flex items-center space-x-2">
            <Waves className="w-8 h-8 text-yenisei-blue" />
            <span className="text-xl font-bold text-gray-800">
              История Енисея
            </span>
          </Link>
          
          {/* Навигационные ссылки (десктоп) */}
          <div className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-yenisei-blue text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
            
            {/* Кнопка "О проекте" */}
            <button
              onClick={onShowWelcome}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
            >
              <Info className="w-5 h-5" />
              <span>О проекте</span>
            </button>
          </div>
          
          {/* Кнопка мобильного меню */}
          <div className="md:hidden">
            <button 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600 hover:text-gray-900 p-2"
            >
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Мобильное меню */}
      {isMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 right-0 bg-white shadow-lg z-50 border-t">
          <div className="px-4 py-2 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={handleNavClick}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-yenisei-blue text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
            
            {/* Кнопка "О проекте" в мобильном меню */}
            <button
              onClick={handleShowWelcome}
              className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors w-full"
            >
              <Info className="w-5 h-5" />
              <span>О проекте</span>
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navigation;