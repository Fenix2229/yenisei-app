import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import { motion } from 'framer-motion';
import { MapPin, Building2, Landmark, Mountain, Navigation } from 'lucide-react';
import { getGeographicPoints } from '../services/api';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Исправление иконок Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const MapPage = () => {
  const [points, setPoints] = useState([]);
  const [filteredPoints, setFilteredPoints] = useState([]);
  const [selectedType, setSelectedType] = useState('all');
  const [loading, setLoading] = useState(true);

  // Координаты течения Енисея (упрощенно)
  const yeniseiRoute = [
    [51.7191, 94.4437], // Кызыл
    [53.7215, 91.4425], // Абакан
    [55.9572, 92.3765], // Дивногорск
    [56.0153, 92.8932], // Красноярск
    [58.4494, 92.1752], // Енисейск
    [58.2343, 92.4833], // Лесосибирск
    [67.4667, 86.5833], // Игарка
    [69.4056, 86.1778], // Дудинка
  ];

  useEffect(() => {
    loadPoints();
  }, []);

  useEffect(() => {
    if (selectedType === 'all') {
      setFilteredPoints(points);
    } else {
      setFilteredPoints(points.filter((p) => p.type === selectedType));
    }
  }, [selectedType, points]);

  const loadPoints = async () => {
    try {
      const response = await getGeographicPoints();
      setPoints(response.data);
      setFilteredPoints(response.data);
    } catch (error) {
      console.error('Ошибка загрузки точек:', error);
    } finally {
      setLoading(false);
    }
  };

  const types = [
    { id: 'all', label: 'Все точки', icon: MapPin },
    { id: 'city', label: 'Города', icon: Building2 },
    { id: 'landmark', label: 'Достопримечательности', icon: Landmark },
    { id: 'nature', label: 'Природа', icon: Mountain },
    { id: 'historical', label: 'Исторические места', icon: Navigation },
  ];

  // Создание кастомных иконок
  const createCustomIcon = (color) => {
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="background-color: ${color}; width: 30px; height: 30px; border-radius: 50% 50% 50% 0; transform: rotate(-45deg); border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>`,
      iconSize: [30, 30],
      iconAnchor: [15, 30],
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-yenisei-blue mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Загрузка карты...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Заголовок */}
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold text-gray-800">
          Интерактивная карта Енисея
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Исследуйте течение великой реки от Саян до Карского моря
        </p>
      </div>

      {/* Фильтры */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Показать на карте:</h2>
        <div className="flex flex-wrap gap-3">
          {types.map((type) => {
            const Icon = type.icon;
            return (
              <motion.button
                key={type.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setSelectedType(type.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedType === type.id
                    ? 'bg-yenisei-blue text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{type.label}</span>
              </motion.button>
            );
          })}
        </div>
      </div>

      {/* Карта */}
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden" style={{ height: '600px' }}>
        <MapContainer
          center={[56.0153, 92.8932]} // Красноярск
          zoom={5}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {/* Линия течения Енисея */}
          <Polyline
            positions={yeniseiRoute}
            color="#1E40AF"
            weight={4}
            opacity={0.7}
          />

          {/* Маркеры точек */}
          {filteredPoints.map((point) => (
            <Marker
              key={point.id}
              position={[point.latitude, point.longitude]}
              icon={createCustomIcon(point.color)}
            >
              <Popup maxWidth={300}>
                <div className="p-2">
                  <h3 className="font-bold text-lg mb-2 text-gray-800">
                    {point.name}
                  </h3>
                  {point.image_url && (
                    <img
                      src={point.image_url}
                      alt={point.name}
                      className="w-full h-32 object-cover rounded-lg mb-2"
                    />
                  )}
                  <p className="text-sm text-gray-600 mb-2">
                    {point.short_description}
                  </p>
                  {point.founding_year && (
                    <p className="text-xs text-gray-500">
                      <strong>Основан:</strong> {point.founding_year} г.
                    </p>
                  )}
                  {point.population && (
                    <p className="text-xs text-gray-500">
                      <strong>Население:</strong> {point.population.toLocaleString()} чел.
                    </p>
                  )}
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Статистика */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white text-center">
          <p className="text-3xl font-bold">{points.filter(p => p.type === 'city').length}</p>
          <p className="text-sm opacity-90 mt-1">Городов</p>
        </div>
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white text-center">
          <p className="text-3xl font-bold">{points.filter(p => p.type === 'nature').length}</p>
          <p className="text-sm opacity-90 mt-1">Природных объектов</p>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white text-center">
          <p className="text-3xl font-bold">{points.filter(p => p.type === 'landmark').length}</p>
          <p className="text-sm opacity-90 mt-1">Достопримечательностей</p>
        </div>
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white text-center">
          <p className="text-3xl font-bold">3487</p>
          <p className="text-sm opacity-90 mt-1">км длина реки</p>
        </div>
      </div>
    </div>
  );
};

export default MapPage;