import type { IFormAuth, LoginResult } from "../../interfaces/forms";
import type { IUserInfo } from "../../interfaces/users";

export const login = async (payload: IFormAuth): Promise<LoginResult> => {
  const url = import.meta.env.VITE_API_URL;

  if (!url) {
    console.error("VITE_API_URL не задано в .env");
    return { status: 500, error: "Серверна конфігурація відсутня" };
  }

  try {
    const res = await fetch(`${url}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    let body: { data?: IUserInfo } | null = null;

    // Спробуємо розпарсити JSON, але не падаємо, якщо не вдалося
    try {
      body = await res.json();
    } catch {
      body = null;
    }

    // Успішний логін
    if (res.status === 200 && body?.data) {
      return {
        status: res.status,
        data: body.data,
      };
    }

    // Помилки від сервера (наприклад, 401, 400 тощо)
    let errorMessage = "Something went wrong!";

    if (body && "error" in body) {
      errorMessage = (body as any).error || errorMessage;
    } else if (body && "message" in body) {
      errorMessage = (body as any).message || errorMessage;
    }

    return {
      status: res.status,
      error: errorMessage,
    };
  } catch (e) {
    const message = e instanceof Error ? e.message : "Network error";
    console.error("Login request failed:", message);
    return { status: 500, error: "Не вдалося підключитися до сервера" };
  }
};