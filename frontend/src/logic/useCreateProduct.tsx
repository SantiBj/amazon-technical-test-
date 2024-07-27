import { useEffect, useState } from "react";
import { useConsult } from "../hooks/useConsult";
import { useNavigate } from "react-router-dom";

interface WarehouseStockType {
  warehouse_id: number;
  quantity: number;
}

interface CreateProductType {
  name: string;
  description: string;
  price: number;
  warehouses: WarehouseStockType[];
}

interface WaterhousesList {
  id: number;
  name: string;
  location: string;
}

const initialData: CreateProductType = {
  name: "",
  description: "",
  price: 0,
  warehouses: [],
};

export function useCreateProduct() {
  const {
    data: waterhouses,
    consult,
    load,
    mssg,
  } = useConsult<WaterhousesList[]>();
  const {
    consult: createConsult,
    load: loadCreate,
    mssg: mssgCreate,
  } = useConsult<WaterhousesList[]>();
  const [data, setData] = useState<CreateProductType>(initialData);
  const [newWarehouse, setNewWarehouse] = useState<WarehouseStockType>({
    warehouse_id: 0,
    quantity: 0,
  });

  const navigate = useNavigate()

  useEffect(() => {
    console.log("consultando");
    consult("inventory/warehouses/", "GET");
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setData({
      ...data,
      [name]: value,
    });
  };

  const handleWarehouseChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setNewWarehouse({
      ...newWarehouse,
      [name]: parseInt(value),
    });
  };

  const addWarehouse = () => {
    setData((prevData) => ({
      ...prevData,
      warehouses: [...prevData.warehouses, newWarehouse],
    }));
    setNewWarehouse({ warehouse_id: 0, quantity: 0 });
  };

  async function create(){
    const product = await createConsult<CreateProductType>("products/create/","POST",data)
    if (product && !mssg){
      navigate("/")
    }
  }

  return {
    data,
    handleChange,
    handleWarehouseChange,
    addWarehouse,
    newWarehouse,
    waterhouses,
    load : load || loadCreate,
    mssg : mssg || mssgCreate,
    create
  };
}
