// Рекомендований сучасний спосіб для роутів у React + TypeScript проєктах

export const Routes = {
  HOME: "/",
  LOGIN: "/login",
  REGISTRATION: "/registration",
  DASHBOARD: "/dashboard",
} as const;

// Тип для значень роутів (для автодоповнення та типобезпеки)
export type Routes = (typeof Routes)[keyof typeof Routes];