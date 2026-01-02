export const healthCheck = async (): Promise<boolean> => {
  const url = import.meta.env.VITE_API_URL;

  if (!url) {
    console.error("VITE_API_URL не задано в .env");
    return false;
  }

  try {
    const res = await fetch(`${url}/api/health_check`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) {
      let errorMessage = "Помилка запиту до сервера";
      try {
        const data = await res.json();
        errorMessage = data.message || errorMessage;
      } catch {
        // Якщо JSON не парситься — ігноруємо
      }

      console.error(`Health check failed: ${res.status} — ${errorMessage}`);
      return false;
    }

    // Якщо статус 2xx — вважаємо, що сервер живий
    return true;
  } catch (err) {
    console.error("Помилка під час health check:", err);
    return false;
  }
};