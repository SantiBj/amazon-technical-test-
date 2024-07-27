import { useParams } from "react-router-dom";
import { Title } from "../components/Title";
import { Loading } from "../components/Loading";
import { AlertError } from "../components/AlertError";
import { useEffect } from "react";
import { Page } from "../components/Page";
import { useConsult } from "../hooks/useConsult";
import { Table } from "../components/InventoryProduct/Table";

interface InventoryItem {
  inventory_id: number;
  name: string;
  location: string;
  quantity_product: number;
}

interface ApiResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: InventoryItem[];
}

export function InventoryProduct() {
  const { productId } = useParams();
  const { data, consult, mssg, load } = useConsult<ApiResponse>();

  useEffect(() => {
    consult("inventory/product-warehouses/" + productId, "GET");
  }, []);

  return (
    <Page>
      <>
        <Title text="Stock en bodegas." />
        <Loading loading={load} />
        <AlertError error={mssg ? true : false} message={mssg} />
        {data !== null && data?.results.length > 0 ? (
          <Table>
            <>
              {data?.results.map((w) => {
                return (
                  <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td className="py-4 px-6">{w.name}</td>
                    <td className="py-4 px-6">{w.location}</td>
                    <td className="py-4 px-6">{w.quantity_product}</td>
                  </tr>
                );
              })}
            </>
          </Table>
        ) : (
          <p>No se encontraron productos</p>
        )}
      </>
    </Page>
  );
}
