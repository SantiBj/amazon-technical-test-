import { Button } from "../components/Button";
import { Input } from "../components/Input";
import { Textarea } from "../components/Textarea";
import { Select } from "../components/Select";
import { Title } from "../components/Title";
import { Page } from "../components/Page";
import { useCreateProduct } from "../logic/useCreateProduct";
import { Loading } from "../components/Loading";
import { AlertError } from "../components/AlertError";
import { AlertInfo } from "../components/AlertInfo";

export function CreateProduct() {
  const {
    data,
    handleChange,
    handleWarehouseChange,
    addWarehouse,
    newWarehouse,
    waterhouses,
    load,
    mssg,
    create,
  } = useCreateProduct();

  return (
    <Page>
      <>
        <Loading loading={load} />
        <section className="space-y-[30px] w-full md:flex md:gap-[20px]">
          <section className="space-y-[30px] md:w-[50%]">
            <Title text="Crear producto" />
            <AlertError error={mssg ? true : false} message={mssg} />
            <section className="space-y-[20px]">
              <Input
                label="Nombre del producto"
                type="text"
                name="name"
                id="name"
                placeholder=""
                handleChange={handleChange}
                value={data.name}
              />
              <Textarea
                label="Descripcion"
                name="description"
                id="description"
                placeholder=""
                handleChange={handleChange}
                value={data.description}
              />
              <Input
                label="Precio del producto"
                type="number"
                name="price"
                id="price"
                placeholder=""
                handleChange={handleChange}
                value={data.price.toString()}
              />
            </section>
          </section>
          <section className="space-y-[30px] md:w-[50%]">
            <Title text="Añadir stock en bodegas" />
            <AlertInfo text="Añade el stock del producto antes de finalizar la creación"/>
            <section>
              {data.warehouses.map((warehouse, index) => (
                <section key={index}>
                  {warehouse.warehouse_id} - {warehouse.quantity}
                </section>
              ))}
            </section>
            <section className="space-y-[20px]">
              <Select
                name="warehouse_id"
                label="Seleccione una bodega"
                handleChange={handleWarehouseChange}
                value={newWarehouse.warehouse_id.toString()}
                options={[
                  {
                    key: "--",
                    value: "--",
                  },
                  ...(waterhouses?.map((w) => ({
                    key: w.id.toString(),
                    value: w.name,
                  })) ?? [
                    {
                      key: "",
                      value: "",
                    },
                  ]),
                ]}
              />
              <Input
                label="Cantidad en stock"
                type="number"
                name="quantity"
                id="quantity"
                placeholder=""
                handleChange={handleWarehouseChange}
                value={newWarehouse.quantity.toString()}
              />
            </section>
            <section className="flex justify-center my-[20px]">
              <Button name="Añadir bodega" onclick={addWarehouse} />
            </section>
          </section>
        </section>
        <section className="flex justify-center my-[20px]">
          <Button name="finalizar creación" onclick={create} />
        </section>
      </>
    </Page>
  );
}
