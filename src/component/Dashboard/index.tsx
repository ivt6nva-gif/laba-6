import React, { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";
import s from "./style.module.css";

import { fetchLocations } from "../../api/locations/locations";
import type { ILocation } from "../../interfaces/locations";

import {
  fetchSensor,
  fetchSensorsList,
  getData,
} from "../../api/sensors/sensors";
import type { ISensorInfo, ISensors } from "../../interfaces/sensors";
type MetricKey =
  | "co_ppm"
  | "humidity_pct"
  | "light_lux"
  | "no2_ppb"
  | "temperature_c"
  | "voltage_v";

const METRICS: { key: MetricKey; label: string; color: string }[] = [
  { key: "temperature_c", label: "Temperature, °C", color: "#34d399" },
  { key: "humidity_pct", label: "Humidity, %", color: "#60a5fa" },
  { key: "voltage_v", label: "Voltage, V", color: "#f97316" },
  { key: "co_ppm", label: "CO, ppm", color: "#facc15" },
  { key: "light_lux", label: "Light, lux", color: "#a855f7" },
  { key: "no2_ppb", label: "NO₂, ppb", color: "#ef4444" },
];

export const Dashboard: React.FC = () => {
  const [selectedMetrics, setSelectedMetrics] = useState<MetricKey[]>([
    "temperature_c",
  ]);

  const [locations, setLocations] = useState<ILocation[]>([]);
  const [sensorsList, setSensorsList] = useState<ISensors[]>([]);
  const [sensorId, setSensorId] = useState<number>(-1);
  const [sensorInfo, setSensorInfo] = useState<ISensorInfo[] | undefined>(undefined);
  const [locationId, setLocationId] = useState<number>(-1);
  const [timeFrom, setTimeFrom] = useState<string>("");
  const [timeTo, setTimeTo] = useState<string>("");
  const [viewData, setViewData] = useState<ISensorInfo[] | undefined>(undefined);

  // Завантажуємо локації при монтуванні
  useEffect(() => {
    fetchLocations().then(setLocations);
  }, []);

  // Завантажуємо список сенсорів при зміні локації
  useEffect(() => {
    if (locationId !== -1) {
      fetchSensorsList(locationId).then(setSensorsList);
    } else {
      setSensorsList([]);
      setSensorId(-1);
    }
  }, [locationId]);

  // Завантажуємо інформацію про сенсор (для підказок дат)
  useEffect(() => {
    if (sensorId !== -1) {
      fetchSensor(sensorId).then(setSensorInfo);
    } else {
      setSensorInfo(undefined);
    }
  }, [sensorId]);

  const toggleMetric = (metric: MetricKey) => {
    setSelectedMetrics((prev) =>
      prev.includes(metric) ? prev.filter((m) => m !== metric) : [...prev, metric]
    );
  };

  const handleApplyFilters = async () => {
    if (sensorId === -1) {
      alert("Оберіть сенсор!");
      return;
    }

    try {
      const data = await getData(sensorId, timeFrom || undefined, timeTo || undefined);
      setViewData(data);
    } catch (err) {
      console.error("Помилка завантаження даних:", err);
      alert("Не вдалося завантажити дані");
    }
  };

  // Дані для графіка
  const chartData = viewData || [];

  return (
    <div className={s.dashboard}>
      <h1>Dashboard</h1>
      <p className={s.subtitle}>A quick overview of your measurements.</p>

      <section className={s.chartSection}>
        <h2>Measurements</h2>
        <p>One flexible chart. Toggle metrics and change filters to explore data.</p>

        {/* Фільтри */}
        <div className={s.filters}>
          <div className={s.filterGroup}>
            <label>Location</label>
            <select value={locationId} onChange={(e) => setLocationId(Number(e.target.value))}>
              <option value={-1}>-----||------</option>
              {locations.map((location) => (
                <option key={location.id} value={location.id}>
                  {location.name}
                </option>
              ))}
            </select>
          </div>

          <div className={s.filterGroup}>
            <label>Sensor</label>
            <select value={sensorId} onChange={(e) => setSensorId(Number(e.target.value))}>
              <option value={-1}>-----||------</option>
              {sensorsList.map((sensor) => (
                <option key={sensor.id} value={sensor.id}>
                  {sensor.code}
                </option>
              ))}
            </select>
          </div>

          <div className={s.filterGroup}>
            <label>From</label>
            <input
              type="datetime-local"
              value={timeFrom}
              onChange={(e) => setTimeFrom(e.target.value)}
              placeholder="YYYY-MM-DD HH:MM:SS"
            />
          </div>

          <div className={s.filterGroup}>
            <label>To</label>
            <input
              type="datetime-local"
              value={timeTo}
              onChange={(e) => setTimeTo(e.target.value)}
              placeholder="YYYY-MM-DD HH:MM:SS"
            />
          </div>

          <button onClick={handleApplyFilters} className={s.applyBtn}>
            Apply
          </button>
        </div>

        {/* Підказки з датами */}
        {sensorInfo && sensorInfo.length > 0 && (
          <div className={s.dateHints}>
            <small>
              Доступні дані з: {sensorInfo[0].ts} до {sensorInfo[sensorInfo.length - 1].ts}
            </small>
          </div>
        )}

        {/* Вибір метрик */}
        <div className={s.metricsToggle}>
          {METRICS.map((m) => (
            <label key={m.key} className={s.metricLabel}>
              <input
                type="checkbox"
                checked={selectedMetrics.includes(m.key)}
                onChange={() => toggleMetric(m.key)}
              />
              <span style={{ color: m.color }}>●</span> {m.label}
            </label>
          ))}
        </div>

        {/* Графік */}
        <div className={s.chartContainer}>
          {chartData.length === 0 ? (
            <p className={s.noData}>Оберіть сенсор та натисніть Apply, щоб побачити дані</p>
          ) : (
            <ResponsiveContainer width="100%" height={500}>
              <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="ts"
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  tick={{ fontSize: 12 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />

                {METRICS.filter((m) => selectedMetrics.includes(m.key)).map((m) => (
                  <Line
                    key={m.key}
                    type="monotone"
                    dataKey={m.key}
                    stroke={m.color}
                    strokeWidth={2}
                    dot={false}
                    name={m.label}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>
    </div>
  );
};

export default Dashboard;