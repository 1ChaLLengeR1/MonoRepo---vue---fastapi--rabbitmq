import { apiSendRequest } from "@/api/common";
import type { bodyCreateUser } from "@/types/global";

export const apiCreateUser = async (body: bodyCreateUser) => {
  const urlPath = `/users`;
  const response = await apiSendRequest(urlPath, "POST", body);
  if (!response || response.status_code > 400) {
    return {
      isValid: false,
      message: response.message,
    };
  }
  return {
    isValid: true,
    message: response.message,
  };
};
