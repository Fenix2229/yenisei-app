import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ChevronLeft, ChevronRight, Filter, Star } from 'lucide-react';
import { getGalleryImages } from '../services/api';

const GalleryPage = () => {
  const [images, setImages] = useState([]);
  const [filteredImages, setFilteredImages] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadImages();
  }, []);

  useEffect(() => {
    if (selectedCategory === 'all') {
      setFilteredImages(images);
    } else if (selectedCategory === 'featured') {
      setFilteredImages(images.filter((img) => img.is_featured));
    } else {
      setFilteredImages(images.filter((img) => img.category === selectedCategory));
    }
  }, [selectedCategory, images]);

  const loadImages = async () => {
    try {
      const response = await getGalleryImages();
      setImages(response.data);
      setFilteredImages(response.data);
    } catch (error) {
      console.error('Ошибка загрузки галереи:', error);
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { id: 'all', label: 'Все фото' },
    { id: 'featured', label: 'Избранное', icon: Star },
    { id: 'nature', label: 'Природа' },
    { id: 'architecture', label: 'Архитектура' },
    { id: 'people', label: 'Люди' },
    { id: 'wildlife', label: 'Дикая природа' },
  ];

  const openLightbox = (image) => {
    setSelectedImage(image);
  };

  const closeLightbox = () => {
    setSelectedImage(null);
  };

  const navigateImage = (direction) => {
    const currentIndex = filteredImages.findIndex((img) => img.id === selectedImage.id);
    let newIndex;

    if (direction === 'next') {
      newIndex = (currentIndex + 1) % filteredImages.length;
    } else {
      newIndex = (currentIndex - 1 + filteredImages.length) % filteredImages.length;
    }

    setSelectedImage(filteredImages[newIndex]);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-yenisei-blue mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Загрузка галереи...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      {/* Заголовок */}
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold text-gray-800">Галерея Енисея</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Красоты Сибири в фотографиях: от величественных гор до северного сияния
        </p>
      </div>

      {/* Фильтры категорий */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <div className="flex items-center space-x-3 mb-4">
          <Filter className="w-6 h-6 text-yenisei-blue" />
          <h2 className="text-xl font-bold text-gray-800">Фильтр по категориям:</h2>
        </div>
        <div className="flex flex-wrap gap-3">
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <motion.button
                key={category.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setSelectedCategory(category.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedCategory === category.id
                    ? 'bg-yenisei-blue text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {Icon && <Icon className="w-5 h-5" />}
                <span>{category.label}</span>
              </motion.button>
            );
          })}
        </div>
      </div>

      {/* Сетка изображений */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AnimatePresence>
          {filteredImages.map((image, index) => (
            <motion.div
              key={image.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ delay: index * 0.05 }}
              className="group cursor-pointer"
              onClick={() => openLightbox(image)}
            >
              <div className="relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300">
                <img
                  src={image.image_url}
                  alt={image.title}
                  className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500"
                />
                
                {/* Избранное */}
                {image.is_featured && (
                  <div className="absolute top-4 right-4 bg-yellow-400 text-white p-2 rounded-full shadow-lg">
                    <Star className="w-5 h-5 fill-current" />
                  </div>
                )}

                {/* Оверлей с информацией */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
                    <h3 className="text-xl font-bold mb-1">{image.title}</h3>
                    <p className="text-sm opacity-90">{image.location}</p>
                    {image.year_taken && (
                      <p className="text-xs opacity-75 mt-1">{image.year_taken} год</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Подпись под фото */}
              <div className="mt-3 px-2">
                <h3 className="font-semibold text-gray-800">{image.title}</h3>
                {image.photographer && (
                  <p className="text-sm text-gray-600">📷 {image.photographer}</p>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Если нет фото */}
      {filteredImages.length === 0 && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg text-center">
          <p className="text-yellow-800 font-semibold">
            В этой категории пока нет фотографий.
          </p>
        </div>
      )}

      {/* Лайтбокс (полноэкранный просмотр) */}
      <AnimatePresence>
        {selectedImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-4"
            onClick={closeLightbox}
          >
            {/* Кнопка закрытия */}
            <button
              onClick={closeLightbox}
              className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors z-10"
            >
              <X className="w-10 h-10" />
            </button>

            {/* Навигация */}
            <button
              onClick={(e) => {
                e.stopPropagation();
                navigateImage('prev');
              }}
              className="absolute left-4 text-white hover:text-gray-300 transition-colors z-10"
            >
              <ChevronLeft className="w-12 h-12" />
            </button>

            <button
              onClick={(e) => {
                e.stopPropagation();
                navigateImage('next');
              }}
              className="absolute right-4 text-white hover:text-gray-300 transition-colors z-10"
            >
              <ChevronRight className="w-12 h-12" />
            </button>

            {/* Изображение и информация */}
            <div
              className="max-w-6xl w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <motion.img
                key={selectedImage.id}
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                src={selectedImage.image_url}
                alt={selectedImage.title}
                className="w-full h-auto max-h-[70vh] object-contain rounded-lg shadow-2xl"
              />

              <div className="mt-6 text-white text-center space-y-2">
                <h2 className="text-3xl font-bold">{selectedImage.title}</h2>
                <p className="text-lg opacity-90">{selectedImage.description}</p>
                <div className="flex justify-center items-center space-x-6 text-sm opacity-75">
                  {selectedImage.photographer && (
                    <span>📷 {selectedImage.photographer}</span>
                  )}
                  {selectedImage.location && <span>📍 {selectedImage.location}</span>}
                  {selectedImage.year_taken && (
                    <span>📅 {selectedImage.year_taken}</span>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default GalleryPage;