import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, XCircle, Volume2, RotateCw, Flag } from 'lucide-react';
import { getRandomQuestions, checkAnswer } from '../services/api';

const QuizPage = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [quizStarted, setQuizStarted] = useState(false);
  const [questionCount, setQuestionCount] = useState(10);
  const [difficulty, setDifficulty] = useState('medium');
  const [results, setResults] = useState([]);
  
  // Максимальное количество вопросов по сложности
  const maxQuestionsByDifficulty = {
    easy: 8,
    medium: 17,
    hard: 5
  };
  
  // Получить максимальное количество вопросов для текущей сложности
  const getMaxQuestions = (diff) => maxQuestionsByDifficulty[diff] || 30;
  
  // Получить доступные варианты количества вопросов для текущей сложности
  const getAvailableQuestionCounts = () => {
    const max = getMaxQuestions(difficulty);
    return [5, 10, 15, 20].filter(num => num <= max);
  };
  
  // Если выбранное количество больше максимума, то уменьшить его
  const getValidQuestionCount = () => {
    const max = getMaxQuestions(difficulty);
    return Math.min(questionCount, max);
  };

  useEffect(() => {
    if (quizStarted) {
      loadQuestions();
    }
  }, [quizStarted, difficulty, questionCount]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      const validCount = getValidQuestionCount();
      const response = await getRandomQuestions({
        count: validCount,
        difficulty: difficulty
      });
      setQuestions(response.data);
      setCurrentQuestionIndex(0);
      setScore(0);
      setAnswered(false);
      setShowResults(false);
      setResults([]);
    } catch (error) {
      console.error('Ошибка загрузки вопросов:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (answer) => {
    if (!answered) {
      setSelectedAnswer(answer);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!selectedAnswer || answered) return;

    try {
      const response = await checkAnswer({
        question_id: questions[currentQuestionIndex].id,
        answer: selectedAnswer
      });

      const resultData = {
        question: questions[currentQuestionIndex].question,
        userAnswer: selectedAnswer,
        correctAnswer: response.data.correct_answer,
        isCorrect: response.data.is_correct,
        explanation: response.data.explanation
      };

      setResults([...results, resultData]);
      setAnswered(true);

      if (response.data.is_correct) {
        setScore(score + response.data.points_earned);
      }
    } catch (error) {
      console.error('Ошибка проверки ответа:', error);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
      setAnswered(false);
    } else {
      setShowResults(true);
    }
  };

  const handleRestart = () => {
    setQuizStarted(false);
    setSelectedAnswer(null);
    setScore(0);
    setAnswered(false);
  };

  const handleStartQuiz = () => {
    setQuizStarted(true);
  };

  if (!quizStarted) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-8 fade-in"
      >
        {/* Заголовок */}
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-bold text-gray-800">
            Викторина "Знаток Енисея"
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Проверьте свои знания об истории, географии и экологии великой сибирской реки
          </p>
        </div>

        {/* Карточка начала викторины */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl p-12 text-white shadow-2xl"
        >
          <div className="space-y-8">
            {/* Параметры викторины */}
            <div className="space-y-6">
              {/* Количество вопросов */}
              <div className="space-y-3">
                <label className="block text-lg font-semibold">
                  📋 Количество вопросов (макс. {getMaxQuestions(difficulty)})
                </label>
                <div className="grid grid-cols-4 gap-3">
                  {[5, 10, 15, 20].map((num) => (
                    <button
                      key={num}
                      onClick={() => {
                        // Если число больше максимума для этой сложности, ограничить его
                        const max = getMaxQuestions(difficulty);
                        setQuestionCount(Math.min(num, max));
                      }}
                      disabled={num > getMaxQuestions(difficulty)}
                      className={`py-3 rounded-lg font-bold transition-all ${
                        questionCount === Math.min(num, getMaxQuestions(difficulty)) && num <= getMaxQuestions(difficulty)
                          ? 'bg-white text-blue-600 scale-105'
                          : num > getMaxQuestions(difficulty)
                          ? 'bg-gray-300 text-gray-500 cursor-not-allowed opacity-50'
                          : 'bg-white/20 hover:bg-white/30'
                      }`}
                      title={num > getMaxQuestions(difficulty) ? `Максимум ${getMaxQuestions(difficulty)} вопросов для этого уровня` : ''}
                    >
                      {num}
                    </button>
                  ))}
                </div>
                {getMaxQuestions(difficulty) < 20 && (
                  <p className="text-sm text-yellow-200">
                    💡 Совет: для этого уровня сложности доступно только {getMaxQuestions(difficulty)} вопросов
                  </p>
                )}
              </div>

              {/* Сложность */}
              <div className="space-y-3">
                <label className="block text-lg font-semibold">
                  ⚡ Сложность
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { value: 'easy', label: '🟢 Легкая (8)' },
                    { value: 'medium', label: '🟡 Средняя (17)' },
                    { value: 'hard', label: '🔴 Сложная (5)' }
                  ].map((option) => (
                    <button
                      key={option.value}
                      onClick={() => {
                        setDifficulty(option.value);
                        // Если текущее количество больше максимума, уменьшить
                        const max = getMaxQuestions(option.value);
                        if (questionCount > max) {
                          setQuestionCount(Math.min(questionCount, max));
                        }
                      }}
                      className={`py-3 rounded-lg font-bold transition-all ${
                        difficulty === option.value
                          ? 'bg-white text-blue-600 scale-105'
                          : 'bg-white/20 hover:bg-white/30'
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Кнопка начала */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleStartQuiz}
              disabled={loading}
              className="w-full bg-white text-blue-600 py-4 rounded-xl font-bold text-lg hover:shadow-lg transition-all disabled:opacity-50"
            >
              {loading ? 'Загрузка вопросов...' : '🚀 Начать викторину'}
            </motion.button>

            {/* Информационные карточки */}
            <div className="grid grid-cols-3 gap-4 pt-4 border-t border-white/30">
              <div className="text-center">
                <p className="text-3xl font-bold">📚</p>
                <p className="text-sm mt-2">Вопросы по истории</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold">🗺️</p>
                <p className="text-sm mt-2">География региона</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold">🌿</p>
                <p className="text-sm mt-2">Экология реки</p>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Загрузка вопросов викторины...</p>
        </div>
      </div>
    );
  }

  if (showResults) {
    const correctAnswers = results.filter(r => r.isCorrect).length;
    const totalQuestions = questions.length;
    // Посчитаем максимум баллов на основе реального количества вопросов и их сложности
    const totalPossiblePoints = results.reduce((acc, r) => {
      const question = questions.find(q => q.question === r.question);
      return acc + (question ? question.points : 10);
    }, 0);
    const percentage = totalPossiblePoints > 0 ? Math.round((score / totalPossiblePoints) * 100) : 0;

    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="space-y-8 fade-in"
      >
        <div className="text-center space-y-6">
          <h1 className="text-5xl font-bold text-gray-800">Результаты викторины</h1>

          {/* Финальный счёт */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="bg-gradient-to-r from-green-400 to-blue-500 rounded-3xl p-12 text-white shadow-2xl"
          >
            <p className="text-7xl font-bold mb-4">{score} / {totalPossiblePoints}</p>
            <p className="text-3xl mb-4">Вы ответили правильно: {correctAnswers} / {totalQuestions}</p>
            
            {/* Оценка */}
            <div className="space-y-4">
              <div className="bg-white/20 rounded-full h-4 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${percentage}%` }}
                  transition={{ duration: 1.5, ease: 'easeOut' }}
                  className="bg-white h-full"
                ></motion.div>
              </div>
              <p className="text-2xl font-bold">
                {percentage >= 80
                  ? '🏆 Отличный результат!'
                  : percentage >= 60
                  ? '👍 Хороший результат!'
                  : percentage >= 40
                  ? '📚 Есть над чем подумать'
                  : '💪 Нужно ещё учиться'}
              </p>
            </div>
          </motion.div>

          {/* Детальные результаты */}
          <div className="space-y-4 max-h-96 overflow-y-auto">
            <h2 className="text-2xl font-bold text-gray-800">Ваши ответы:</h2>
            <AnimatePresence>
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className={`p-4 rounded-lg text-left ${
                    result.isCorrect ? 'bg-green-100 border-l-4 border-green-500' : 'bg-red-100 border-l-4 border-red-500'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <p className="font-semibold text-gray-800">Вопрос {index + 1}</p>
                    {result.isCorrect ? (
                      <CheckCircle className="text-green-600 w-6 h-6" />
                    ) : (
                      <XCircle className="text-red-600 w-6 h-6" />
                    )}
                  </div>
                  <p className="text-gray-700 mb-2">{result.question}</p>
                  <p className="text-sm text-gray-600 mb-2">
                    <strong>Ваш ответ:</strong> {result.userAnswer}
                    {!result.isCorrect && ` (правильно: ${result.correctAnswer})`}
                  </p>
                  {result.explanation && (
                    <p className="text-sm text-gray-700 italic">{result.explanation}</p>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          {/* Кнопки действия */}
          <div className="flex gap-4 justify-center pt-6">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleRestart}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700 transition-all flex items-center gap-2"
            >
              <RotateCw className="w-5 h-5" />
              Пройти снова
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => window.location.href = '/'}
              className="bg-gray-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-gray-700 transition-all"
            >
              На главную
            </motion.button>
          </div>
        </div>
      </motion.div>
    );
  }

  if (!questions.length) {
    return (
      <div className="text-center py-12">
        <p className="text-xl text-gray-600">Не удалось загрузить вопросы</p>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-8 fade-in"
    >
      {/* Прогресс и информация */}
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <p className="text-gray-600">
              Вопрос {currentQuestionIndex + 1} из {questions.length}
            </p>
            <h2 className="text-3xl font-bold text-gray-800">Викторина "Знаток Енисея"</h2>
          </div>
          <div className="text-center bg-blue-600 text-white rounded-full p-6">
            <p className="text-3xl font-bold">{score}</p>
            <p className="text-sm">баллов</p>
          </div>
        </div>

        {/* Прогресс бар */}
        <div className="space-y-2">
          <div className="bg-gray-200 rounded-full h-3 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
              className="bg-blue-600 h-full"
            ></motion.div>
          </div>
        </div>
      </div>

      {/* Контейнер вопроса */}
      <motion.div
        key={currentQuestionIndex}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="bg-white rounded-2xl p-8 shadow-lg space-y-6"
      >
        {/* Вопрос */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-bold text-gray-800">
              {currentQuestion.question}
            </h3>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
              currentQuestion.difficulty === 'easy'
                ? 'bg-green-100 text-green-800'
                : currentQuestion.difficulty === 'medium'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-red-100 text-red-800'
            }`}>
              {currentQuestion.difficulty === 'easy' ? '🟢' : currentQuestion.difficulty === 'medium' ? '🟡' : '🔴'} {
                currentQuestion.difficulty === 'easy' ? 'Легко' : currentQuestion.difficulty === 'medium' ? 'Средне' : 'Сложно'
              }
            </span>
          </div>
        </div>

        {/* Варианты ответов */}
        <div className="space-y-3">
          {['option_a', 'option_b', 'option_c', 'option_d'].map((option, index) => {
            const answerKey = String.fromCharCode(65 + index); // A, B, C, D
            const isSelected = selectedAnswer === answerKey;
            const isCorrect = currentQuestion.correct_answer === answerKey;
            const showCorrect = answered && isCorrect;
            const showWrong = answered && isSelected && !isCorrect;

            return (
              <motion.button
                key={option}
                whileHover={!answered ? { scale: 1.02 } : {}}
                whileTap={!answered ? { scale: 0.98 } : {}}
                onClick={() => handleAnswerSelect(answerKey)}
                disabled={answered}
                className={`w-full p-4 rounded-lg text-left font-semibold transition-all border-2 ${
                  showWrong
                    ? 'bg-red-100 border-red-500 text-red-900'
                    : showCorrect
                    ? 'bg-green-100 border-green-500 text-green-900'
                    : isSelected
                    ? 'bg-blue-100 border-blue-500 text-blue-900'
                    : 'bg-gray-50 border-gray-200 hover:border-blue-300 text-gray-800'
                } disabled:cursor-not-allowed`}
              >
                <div className="flex items-center justify-between">
                  <span>
                    <strong className="text-lg">{answerKey}.</strong> {currentQuestion[option]}
                  </span>
                  {showCorrect && <CheckCircle className="text-green-600 w-6 h-6" />}
                  {showWrong && <XCircle className="text-red-600 w-6 h-6" />}
                </div>
              </motion.button>
            );
          })}
        </div>

        {/* Объяснение (если ответ дан) */}
        <AnimatePresence>
          {answered && currentQuestion.explanation && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded"
            >
              <p className="text-sm text-gray-700">
                <strong>💡 Объяснение:</strong> {currentQuestion.explanation}
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Кнопки действия */}
        <div className="flex gap-4 pt-6 border-t">
          {!answered ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSubmitAnswer}
              disabled={!selectedAnswer}
              className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 transition-all disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              ✓ Ответить
            </motion.button>
          ) : (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleNextQuestion}
              className="flex-1 bg-green-600 text-white py-3 rounded-lg font-bold hover:bg-green-700 transition-all"
            >
              {currentQuestionIndex < questions.length - 1 ? 'Далее →' : '📊 Смотреть результаты'}
            </motion.button>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default QuizPage;