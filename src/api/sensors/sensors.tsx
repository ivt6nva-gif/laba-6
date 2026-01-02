import type { IRes } from "../../interfaces/response";
import type { ISensors,  ISensorInfo } from "../../interfaces/sensors";

export const fetchSensorsList = async (
  location_id: number
): Promise<ISensors[]> => {
  const url = import.meta.env.VITE_API_URL;

  const res = await fetch(`${url}/api/sensors/all/location/${location_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(
      `Failed to fetch sensors for location ${location_id}: ${res.status} ${res.statusText}`
    );
  }

  const body: IRes<ISensors[]> = await res.json();
  return body.data;
};

export const fetchSensor = async (
  sensor_id: number
): Promise< ISensorInfo[]> => {
  const url = import.meta.env.VITE_API_URL;
  
  const res = await fetch(`${url}/api/sensors/measurements/${sensor_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(
      `Failed to fetch sensor ${sensor_id}: ${res.status} ${res.statusText}`
    );
  }

  const body: IRes< ISensorInfo[]> = await res.json();
  return body.data;
};

export const getData = async (
  sensor_id: number,
  time_from?: string,
  time_to?: string
): Promise<ISensorInfo[]> => {
  const baseUrl = import.meta.env.VITE_API_URL;
  // Helper: convert `datetime-local` value (e.g. 2025-12-14T12:34:56.123)
  // into backend format `YYYY-MM-DD HH:MM:SS` (remove fractional seconds)
  const formatForBackend = (v?: string) => {
    if (!v) return undefined;
    // If already contains space, assume it's OK
    if (v.includes(" ")) return v.split(".")[0];
    // Replace T with space and strip fractional seconds
    const s = v.replace("T", " ");
    return s.split(".")[0];
  };

  const tf = formatForBackend(time_from);
  const tt = formatForBackend(time_to);

  let url = `${baseUrl}/api/sensors/measurements?sensor_id=${sensor_id}`;
  if (tf) url += `&time_from=${encodeURIComponent(tf)}`;
  if (tt) url += `&time_to=${encodeURIComponent(tt)}`;

  const res = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(
      `Failed to fetch measurements for sensor ${sensor_id}: ${res.status} ${res.statusText}`
    );
  }

  const body: IRes<ISensorInfo[]> = await res.json();
  return body.data;
};