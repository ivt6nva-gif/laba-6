import type { IUserInfo } from "./users";

export interface IFormAuth {
  username: string;
  password: string;
}

export type LoginResponse =
  | { data?: IUserInfo }
  | { error: string; details?: number }
  | undefined
  | null;

export type LoginResult =
  | {
      status: number;
      data: IUserInfo;
    }
  | {
      status: number;
      error: string;
    };

export interface RegisterPayload {
  username: string;
  password: string;
}

export interface RegistrationSuccessResponse {
  message: string;
}

export type RegisterResult =
  | { data: RegistrationSuccessResponse }
  | { error: string; status?: number };