import type { ResponseApi } from "@/types/global";

const urlApi: string = "http://127.0.0.1:3000";

export const apiSendRequest = async (
  urlPath: string,
  method: "POST" | "PATCH" | "DELETE" = "POST",
  body: object,
  lvl: number = 0
): Promise<ResponseApi> => {
  try {
    const url: string = `${urlApi}${urlPath}`;
    const response = await fetch(url, {
      method: method,
      body: JSON.stringify(body),
    });

    const responseData: ResponseApi = await response.json();
    return responseData;
  } catch (error) {
    if (lvl < 3) {
      await new Promise((resolve) => setTimeout(resolve, 3000));
      return apiSendRequest(urlPath, method, body, lvl + 1);
    } else {
      console.error(`apiSendRequest: ${urlPath} is not working`);
      throw error;
    }
  }
};

export const apiGetRequest = async (
  urlPath: string,
  lvl: number = 0
): Promise<ResponseApi> => {
  try {
    const url: string = `${urlApi}${urlPath}`;
    const response = await fetch(url, {
      method: "GET",
    });

    const responseData: ResponseApi = await response.json();
    return responseData;
  } catch (error) {
    if (lvl < 3) {
      await new Promise((resolve) => setTimeout(resolve, 3000));
      return apiGetRequest(urlPath, lvl + 1);
    } else {
      console.error(`apiGetRequest: ${urlPath} is not working`);
      throw error;
    }
  }
};
