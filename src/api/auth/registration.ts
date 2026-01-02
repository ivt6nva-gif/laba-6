import type {
  RegisterPayload,
  RegisterResult,
  RegistrationSuccessResponse,
} from "../../interfaces/forms";

export const register = async (payload: RegisterPayload): Promise<RegisterResult> => {
  const baseUrl = import.meta.env.VITE_API_URL;

  if (!baseUrl) {
    console.error("VITE_API_URL не задано в .env");
    return { error: "Серверна конфігурація відсутня (VITE_API_URL)" };
  }

  try {
    const res = await fetch(`${baseUrl}/api/auth/registration`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    let json: unknown = null;

    // Спробуємо розпарсити JSON, але не падаємо, якщо не вдалося
    try {
      json = await res.json();
    } catch {
      json = null;
    }

    // Успішна реєстрація (зазвичай 201 Created або 200 OK)
    if ((res.status === 200 || res.status === 201) && json) {
      const data = json as Partial<RegistrationSuccessResponse>;
      return {
        data: {
          message: data?.message || "Користувача успішно створено",
        },
      };
    }

    // Обробка помилок від бекенду
    const errJson = json as { message?: string; detail?: string; error?: string } | null;
    const backendMsg = errJson?.message || errJson?.detail || errJson?.error || null;

    if (res.status === 400) {
      return {
        status: res.status,
        error: backendMsg || "Невірні дані для реєстрації",
      };
    }

    if (res.status === 409) {
      return {
        status: res.status,
        error: backendMsg || "Користувач з таким username вже існує",
      };
    }

    if (res.status === 401 || res.status === 403) {
      return {
        status: res.status,
        error: backendMsg || "Немає доступу до операції реєстрації",
      };
    }

    if (res.status >= 500) {
      return {
        status: res.status,
        error: backendMsg || "Внутрішня помилка сервера",
      };
    }

    // Будь-який інший статус
    return {
      status: res.status,
      error:
        backendMsg ||
        `Неочікувана відповідь від сервера: HTTP ${res.status}`,
    };
  } catch (e) {
    const message = e instanceof Error ? e.message : "Мережева помилка";
    console.error("Помилка під час реєстрації:", message);
    return { error: "Не вдалося підключитися до сервера" };
  }
};