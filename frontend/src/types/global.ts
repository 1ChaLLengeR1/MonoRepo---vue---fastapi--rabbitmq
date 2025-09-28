export type user = {
  id: string;
  name: string;
  lastname: string;
  email: string;
  age: string;
  city: string;
};

export type userTask = {
  id: string;
  task_id: string;
  status: string;
  result: string;
};

export interface ResponseApi {
  message: string;
  status_code: number;
  status?: string;
  users?: user[] | userTask[];
  count: number;
  task_id?: string;
  result?: string;
}

export type bodyCreateUser = {
  name: string;
  lastname: string;
  email: string;
  age: string;
  city: string;
};
