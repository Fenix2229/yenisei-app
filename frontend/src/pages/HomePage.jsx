import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Clock, Map, Image, Brain, Sparkles } from 'lucide-react';
import { getRandomFact, getImportantEvents } from '../services/api';

const HomePage = () => {
  const [fact, setFact] = useState(null);
  const [events, setEvents] = useState([]);
  
  useEffect(() => {
    // Загружаем случайный факт
    getRandomFact()
      .then(res => setFact(res.data))
      .catch(err => console.error(err));
      
    // Загружаем важные события
    getImportantEvents(3)
      .then(res => setEvents(res.data))
      .catch(err => console.error(err));
  }, []);
  
  const features = [
    {
      icon: Clock,
      title: 'Лента времени',
      description: 'Путешествие сквозь века истории Енисея',
      link: '/timeline',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: Map,
      title: 'Интерактивная карта',
      description: 'Исследуйте течение великой реки',
      link: '/map',
      color: 'from-green-500 to-green-600'
    },
    {
      icon: Image,
      title: 'Галерея',
      description: 'Красоты Сибири в фотографиях',
      link: '/gallery',
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: Brain,
      title: 'Викторина',
      description: 'Проверьте свои знания о Енисее',
      link: '/quiz',
      color: 'from-orange-500 to-orange-600'
    }
  ];
  
  return (
    <div className="space-y-12 fade-in">
      {/* Герой секция */}
      <div className="text-center space-y-6">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-800">
          Река <span className="text-yenisei-blue">Енисей</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Познакомьтесь с историей одной из величайших рек планеты — 
          от древних времён до современности
        </p>
      </div>
      
      {/* Интересный факт */}
      {fact && (
        <div className="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-2xl p-8 text-white shadow-xl">
          <div className="flex items-start space-x-4">
            <Sparkles className="w-8 h-8 flex-shrink-0 mt-1" />
            <div>
              <h3 className="text-2xl font-bold mb-2">{fact.title}</h3>
              <p className="text-lg opacity-95">{fact.fact}</p>
            </div>
          </div>
        </div>
      )}
      
      {/* Основные разделы */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon;
          return (
            <Link
              key={feature.link}
              to={feature.link}
              className="group"
            >
              <div className={`bg-gradient-to-br ${feature.color} rounded-2xl p-8 text-white shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2`}>
                <Icon className="w-12 h-12 mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="text-2xl font-bold mb-2">{feature.title}</h3>
                <p className="text-white/90">{feature.description}</p>
              </div>
            </Link>
          );
        })}
      </div>
      
      {/* Важные события */}
      {events.length > 0 && (
        <div className="bg-white rounded-2xl p-8 shadow-lg">
          <h2 className="text-3xl font-bold text-gray-800 mb-6">
            Ключевые события истории
          </h2>
          <div className="space-y-4">
            {events.map((event) => (
              <div
                key={event.id}
                className="border-l-4 border-yenisei-blue pl-4 py-2 hover:bg-gray-50 transition-colors"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-800">
                      {event.title}
                    </h3>
                    <p className="text-gray-600 mt-1">
                      {event.short_description}
                    </p>
                  </div>
                  <span className="text-yenisei-blue font-bold text-lg whitespace-nowrap ml-4">
                    {event.date_description}
                  </span>
                </div>
              </div>
            ))}
          </div>
          <Link
            to="/timeline"
            className="inline-block mt-6 px-6 py-3 bg-yenisei-blue text-white rounded-lg hover:bg-yenisei-dark transition-colors"
          >
            Смотреть всю историю →
          </Link>
        </div>
      )}
    </div>
  );
};

export default HomePage;