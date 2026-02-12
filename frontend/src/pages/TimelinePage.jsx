import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, ChevronDown, ChevronUp, Info } from 'lucide-react';
import { getEpochs, getEpochWithEvents } from '../services/api';

const TimelinePage = () => {
  const [epochs, setEpochs] = useState([]);
  const [selectedEpoch, setSelectedEpoch] = useState(null);
  const [expandedEvent, setExpandedEvent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEpochs();
  }, []);

  const loadEpochs = async () => {
    try {
      const response = await getEpochs();
      setEpochs(response.data);
      if (response.data.length > 0) {
        loadEpochEvents(response.data[0].id);
      }
    } catch (error) {
      console.error('Ошибка загрузки эпох:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadEpochEvents = async (epochId) => {
    try {
      const response = await getEpochWithEvents(epochId);
      setSelectedEpoch(response.data);
      setExpandedEvent(null);
    } catch (error) {
      console.error('Ошибка загрузки событий:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-yenisei-blue mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Загрузка истории...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      {/* Заголовок */}
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold text-gray-800">
          Лента времени
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Путешествие сквозь века: от древних поселений до современной эпохи
        </p>
      </div>

      {/* Селектор эпох */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
          <Calendar className="w-6 h-6 mr-2 text-yenisei-blue" />
          Исторические эпохи
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {epochs.map((epoch) => (
            <motion.button
              key={epoch.id}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => loadEpochEvents(epoch.id)}
              className={`p-4 rounded-xl text-left transition-all duration-300 ${
                selectedEpoch?.id === epoch.id
                  ? 'ring-4 ring-yenisei-blue shadow-xl'
                  : 'hover:shadow-lg'
              }`}
              style={{
                background: selectedEpoch?.id === epoch.id
                  ? epoch.color
                  : `${epoch.color}20`,
                borderLeft: `4px solid ${epoch.color}`,
              }}
            >
              <h3
                className={`font-bold text-lg mb-2 ${
                  selectedEpoch?.id === epoch.id ? 'text-white' : 'text-gray-800'
                }`}
              >
                {epoch.name}
              </h3>
              <p
                className={`text-sm ${
                  selectedEpoch?.id === epoch.id ? 'text-white/90' : 'text-gray-600'
                }`}
              >
                {epoch.start_year < 0 ? `${Math.abs(epoch.start_year)} до н.э.` : epoch.start_year} 
                {' — '}
                {epoch.end_year < 0 ? `${Math.abs(epoch.end_year)} до н.э.` : epoch.end_year}
              </p>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Описание выбранной эпохи */}
      {selectedEpoch && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-8 text-white shadow-xl"
        >
          <h2 className="text-3xl font-bold mb-4">{selectedEpoch.name}</h2>
          <p className="text-lg leading-relaxed opacity-95">
            {selectedEpoch.description}
          </p>
        </motion.div>
      )}

      {/* Таймлайн событий */}
      {selectedEpoch && selectedEpoch.events && (
        <div className="relative">
          {/* Вертикальная линия таймлайна */}
          <div
            className="absolute left-8 top-0 bottom-0 w-1 rounded-full"
            style={{ backgroundColor: selectedEpoch.color }}
          />

          <div className="space-y-8">
            <AnimatePresence>
              {selectedEpoch.events.map((event, index) => (
                <motion.div
                  key={event.id}
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 50 }}
                  transition={{ delay: index * 0.1 }}
                  className="relative pl-20"
                >
                  {/* Точка на линии */}
                  <div
                    className="absolute left-5 top-6 w-7 h-7 rounded-full border-4 border-white shadow-lg"
                    style={{ backgroundColor: selectedEpoch.color }}
                  />

                  {/* Карточка события */}
                  <div className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
                    <div className="md:flex">
                      {/* Изображение */}
                      {event.image_url && (
                        <div className="md:w-1/3 relative overflow-hidden">
                          <img
                            src={event.image_url}
                            alt={event.title}
                            className="w-full h-full object-cover hover:scale-110 transition-transform duration-500"
                          />
                          <div className="absolute top-4 left-4 bg-black/70 text-white px-3 py-1 rounded-full text-sm font-semibold">
                            {event.date_description}
                          </div>
                        </div>
                      )}

                      {/* Контент */}
                      <div className="p-6 md:w-2/3">
                        <div className="flex justify-between items-start mb-3">
                          <h3 className="text-2xl font-bold text-gray-800">
                            {event.title}
                          </h3>
                          <span className="text-sm font-semibold text-white px-3 py-1 rounded-full bg-gradient-to-r from-orange-400 to-pink-500">
                            Важность: {event.importance}/10
                          </span>
                        </div>

                        <p className="text-gray-600 mb-4 leading-relaxed">
                          {expandedEvent === event.id
                            ? event.description
                            : event.short_description}
                        </p>

                        {event.image_caption && (
                          <p className="text-sm text-gray-500 italic mb-4">
                            📷 {event.image_caption}
                          </p>
                        )}

                        {/* Кнопка "Читать далее" */}
                        {event.description !== event.short_description && (
                          <button
                            onClick={() =>
                              setExpandedEvent(
                                expandedEvent === event.id ? null : event.id
                              )
                            }
                            className="flex items-center space-x-2 text-yenisei-blue hover:text-yenisei-dark font-semibold transition-colors"
                          >
                            {expandedEvent === event.id ? (
                              <>
                                <ChevronUp className="w-5 h-5" />
                                <span>Свернуть</span>
                              </>
                            ) : (
                              <>
                                <Info className="w-5 h-5" />
                                <span>Читать полностью</span>
                              </>
                            )}
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      )}

      {/* Если нет событий */}
      {selectedEpoch && (!selectedEpoch.events || selectedEpoch.events.length === 0) && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
          <p className="text-yellow-800 font-semibold">
            В этой эпохе пока нет записанных событий.
          </p>
        </div>
      )}
    </div>
  );
};

export default TimelinePage;