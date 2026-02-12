import { motion } from 'framer-motion';

const WelcomeScreen = ({ onClose }) => {
  const handleContinue = () => {
    localStorage.setItem('welcomeShown', 'true');
    onClose();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', damping: 20 }}
        className="bg-white rounded-3xl p-12 max-w-2xl mx-4 text-center shadow-2xl"
      >
        {/* Заголовок */}
        <motion.h1
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-4xl md:text-5xl font-bold text-gray-800 mb-8"
        >
          История реки <span className="text-blue-600">Енисей</span>
        </motion.h1>

        {/* Основной текст */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="space-y-6 my-8"
        >
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 text-lg leading-relaxed text-gray-700">
            <p className="font-semibold text-xl mb-4">
              Проект по истории
            </p>
            <p className="mb-3">
              <strong>Ученика 9А класса</strong><br />
              Пьянова Александра Григорьевича
            </p>
            <p className="mb-3">
              <strong>Предмет:</strong> История
            </p>
            <p className="mb-3">
              <strong>Учебный год:</strong> 2025 - 2026
            </p>
            <p>
              <strong>Преподаватель:</strong><br />
              Шишлова Дарья Евгеньевна
            </p>
          </div>

          <p className="text-gray-600 text-base">
            Познакомьтесь с историей одной из величайших рек планеты — 
            от древних времён до современности
          </p>
        </motion.div>

        {/* Кнопка */}
        <motion.button
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.6 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleContinue}
          className="mt-8 bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transition-all"
        >
          Далее →
        </motion.button>
      </motion.div>
    </motion.div>
  );
};

export default WelcomeScreen;
