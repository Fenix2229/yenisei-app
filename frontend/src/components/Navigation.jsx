import { Link, useLocation } from 'react-router-dom';
import { Home, Clock, Map, Image, Brain, Waves, Info } from 'lucide-react';

const Navigation = ({ onShowWelcome }) => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: Home, label: 'Главная' },
    { path: '/timeline', icon: Clock, label: 'Лента времени' },
    { path: '/map', icon: Map, label: 'Карта' },
    { path: '/gallery', icon: Image, label: 'Галерея' },
    { path: '/quiz', icon: Brain, label: 'Викторина' },
  ];
  
  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Логотип */}
          <Link to="/" className="flex items-center space-x-2">
            <Waves className="w-8 h-8 text-yenisei-blue" />
            <span className="text-xl font-bold text-gray-800">
              История Енисея
            </span>
          </Link>
          
          {/* Навигационные ссылки */}
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
          
          {/* Мобильное меню (упрощенное) */}
          <div className="md:hidden">
            <button className="text-gray-600 hover:text-gray-900">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;