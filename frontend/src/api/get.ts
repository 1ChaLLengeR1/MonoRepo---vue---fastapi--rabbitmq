import { apiGetRequest } from "@/api/common";

export const apiCollectionUsers = async () => {
  const urlPath = `/users/collection`;
  const response = await apiGetRequest(urlPath);
  if (!response || response.status_code > 400) {
    return {
      isValid: false,
      message: response.message,
      users: [],
    };
  }
  return {
    isValid: true,
    message: response.message,
    users: response.users,
  };
};

export const apiCollectionTasks = async () => {
  const urlPath = `/tasks/collection`;
  const response = await apiGetRequest(urlPath);
  if (!response || response.status_code > 400) {
    return {
      isValid: false,
      message: response.message,
      users: [],
    };
  }
  return {
    isValid: true,
    message: response.message,
    users: response.users,
  };
};

export const apiOneTask = async (taskId: string) => {
  const urlPath = `/task/${taskId}`;
  const response = await apiGetRequest(urlPath);
  if (!response || response.status_code > 400) {
    return {
      isValid: false,
      status: response.status,
      result: response.result,
    };
  }
  return {
    isValid: true,
    status: response.status,
    result: response.result,
  };
};
