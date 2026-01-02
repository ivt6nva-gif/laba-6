export interface ISensors {
  code: string;
  fw_version: string;
  id: number;
  location_id: number;
  serial: string;
  type: string;
}

export interface ISensorInfo {
  co_ppm: number;
  humidity_pct: number;
  light_lux: number;
  no2_ppb: number;
  sensor_id: number;
  temperature_c: number;
  ts: string;
  voltage_v: number;
}