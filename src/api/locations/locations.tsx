import type { ILocation } from "../../interfaces/locations";
import type { IRes } from "../../interfaces/response";

// Припускаємо, що IRes виглядає так:
// interface IRes<T = unknown> {
//   data: T;
//   error?: string;
// }

export const fetchLocations = async (): Promise<ILocation[]> => {
  const baseUrl = import.meta.env.VITE_API_URL;

  if (!baseUrl) {
    throw new Error("VITE_API_URL не заданий у змінних середовища");
  }

  const url = `${baseUrl}/api/locations/all`;

  try {
    const res = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) {
      throw new Error(`Помилка завантаження локацій: ${res.status} ${res.statusText}`);
    }

    const body: IRes<ILocation[]> = await res.json();

    // Додаткова перевірка структури відповіді (рекомендовано)
    if (!body || !Array.isArray(body.data)) {
      throw new Error("Невірний формат відповіді від сервера");
    }

    return body.data;
  } catch (error) {
    console.error("Помилка при fetchLocations:", error);
    // Перекидаємо помилку далі, щоб компонент міг її обробити
    throw error instanceof Error ? error : new Error("Невідома помилка мережі");
  }
};