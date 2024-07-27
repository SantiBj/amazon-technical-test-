import axios, { AxiosResponse } from "axios";
import { URL_BASE } from "../config";
import { useState } from "react";

export type MethodType = "GET" | "PATCH" | "POST" | "PUT" | "DELETE";

export function useConsult<TypeResponse>() {
  const [data, setData] = useState<TypeResponse | null>(null);
  const [load, setLoad] = useState(false);
  const [mssg, setMssg] = useState<string | null>(null);

  function resetAll(): void {
    setData(null);
    setMssg(null);
  }

  async function consult<TypeBody>(
    url: string,
    method: MethodType,
    body: TypeBody | null = null
  ) {
    try {
      setLoad(true);
      const res: AxiosResponse<TypeResponse> = await axios.request({
        url: URL_BASE + url,
        method: method,
        data: method == "GET" ? null : body,
      });
      setData(res.data);
      return res.data
    } catch (error: any) {
        if (error.response) {
          const errorDetails = JSON.stringify(error.response.data);
          setMssg(errorDetails);
        }
      }
      finally {
      setLoad(false);
    }
  }

  return {
    data,
    consult,
    load,
    mssg,
    resetAll,
  };
}
