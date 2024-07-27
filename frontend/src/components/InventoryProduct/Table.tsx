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
                      Nombre de la bodega
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Ubicación
                    </th>
                    <th scope="col" className="py-3 px-6">
                      Cantidad
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
