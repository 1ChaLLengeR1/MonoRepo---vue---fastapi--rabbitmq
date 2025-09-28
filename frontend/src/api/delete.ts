import { apiSendRequest } from "@/api/common";

export const apiDeleteUser = async (userId: string) => {
  const urlPath = `/users/delete/${userId}`;
  const response = await apiSendRequest(urlPath, "DELETE", {});
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
