import { useEffect } from "react";
import { Table } from "../components/home/Table";
import { Page } from "../components/Page";
import { Title } from "../components/Title";
import { useConsult } from "../hooks/useConsult";
import { AlertError } from "../components/AlertError";
import { Loading } from "../components/Loading";
import { Link } from "react-router-dom";

interface Product {
  product_id: number;
  product_name: string;
  product_description: string;
  product_price: string;
  total_quantity: number;
}

interface ApiResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Product[];
}

export function Home() {
  const { data, consult, mssg, load } = useConsult<ApiResponse>();

  useEffect(() => {
    consult("products/", "GET");
  }, []);

  return (
    <Page>
      <section>
        <Title text="Productos Disponibles." />
        <Loading loading={load} />
        <AlertError error={mssg ? true : false} message={mssg} />
        {data !== null && data?.results.length > 0 ? (
          <Table>
            <>
              {data?.results.map((product) => {
                return (
                  <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td className="py-4 px-6">{product.product_name}</td>
                    <td className="py-4 px-6">{product.product_description}</td>
                    <td className="py-4 px-6">{product.product_price}</td>
                    <td className="py-4 px-6">{product.total_quantity}</td>
                    <td className="py-4 px-6">
                      <section className="p-[8px] text-center border-black border-[2px] rounded-md">
                        <Link to={`/inventory/${product.product_id}`}>Ver inventario</Link>
                      </section>
                    </td>
                    <td className="py-4 px-6">Añadir al carrito</td>
                    <td className="py-4 px-6">Editar</td>
                  </tr>
                );
              })}
            </>
          </Table>
        ) : (
          <p>No se encontraron productos</p>
        )}
      </section>
    </Page>
  );
}
