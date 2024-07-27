storage_procedure_proccess_sale = '''
CREATE TYPE public.sale_products_type AS (
    inventory_id int4,
    quantity int4
);

CREATE OR REPLACE FUNCTION process_sale(
    sale_items public.sale_products_type[]
)
RETURNS VOID
LANGUAGE plpgsql
AS $function$
DECLARE
    sale_id INT;
    inventory_record RECORD;
    item public.sale_products_type;
    item_price DECIMAL;
    item_subtotal DECIMAL;
    sale_total DECIMAL := 0;
BEGIN
    -- Crear la venta con un total inicial de 1 porque tiene un check que indica que debe ser mayor a 0
    INSERT INTO sales (total, creation_date)
    VALUES (1, NOW())
    RETURNING id INTO sale_id;

    -- Iterar sobre los elementos de la venta
    FOREACH item IN ARRAY sale_items
    LOOP
        -- Verificar si el inventario existe
        SELECT * INTO inventory_record FROM inventory
        WHERE id = item.inventory_id;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'Inventory with ID % does not exist', item.inventory_id;
        END IF;

        -- Verificar si hay suficiente cantidad en el inventario
        IF inventory_record.quantity < item.quantity THEN
            RAISE EXCEPTION 'Not enough quantity for Inventory ID %', item.inventory_id;
        END IF;

        -- Obtener el precio del producto
        SELECT price INTO item_price FROM products
        WHERE id = inventory_record.product_id;

        -- Calcular el subtotal para el item
        item_subtotal := item_price * item.quantity;

        -- Insertar el item en la tabla items_sales
        INSERT INTO items_sales (product_inventory_id, sale_id, quantity, price_product, subtotal)
        VALUES (
            item.inventory_id,
            sale_id,
            item.quantity,
            item_price,
            item_subtotal
        );

        -- Actualizar la cantidad en el inventario
        UPDATE inventory
        SET quantity = quantity - item.quantity
        WHERE id = item.inventory_id;

        -- Sumar el subtotal al total de la venta
        sale_total := sale_total + item_subtotal;
    END LOOP;

    -- Actualizar el total de la venta en la tabla sales
    UPDATE sales
    SET total = sale_total
    WHERE id = sale_id;
END;
$function$;

'''