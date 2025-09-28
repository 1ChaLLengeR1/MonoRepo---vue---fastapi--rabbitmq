import { apiSendRequest } from "@/api/common";
import type { bodyCreateUser } from "@/types/global";

export const apiPatchUser = async (userId: string, body: bodyCreateUser) => {
  const urlPath = `/users/update/${userId}`;
  const response = await apiSendRequest(urlPath, "POST", body);
  if (!response || response.status_code > 400) {
    return {
      isValid: false,
      status_code: response.status_code,
      task_id: response.task_id,
    };
  }
  return {
    isValid: true,
    status_code: response.status_code,
    task_id: response.task_id,
  };
};
