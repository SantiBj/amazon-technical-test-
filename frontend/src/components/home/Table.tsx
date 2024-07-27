import { ReactElement } from "react";

export function Table({ children }: { children: ReactElement }) {
  return (
    <>
        <div className="flex items-center justify-center min-h-[450px] my-[30px]">
          <div className="overflow-x-auto relative shadow-md sm:rounded-lg">
            <div className="overflow-x-auto relative shadow-md sm:rounded-lg">
              <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                    <th scope="col" className="py-3 px-6">
                      Nombre del producto
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Descripcion
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Precio Unitario
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Cantidad total en inventario
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Inventario
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Vender
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Editar
                    </th>
                  </tr>
                </thead>
                <tbody>{children}</tbody>
              </table>
            </div>
          </div>
        </div>
    </>
  );
}
