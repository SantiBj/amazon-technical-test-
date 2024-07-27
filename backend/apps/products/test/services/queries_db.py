storage_procedure_proccess_create_product = '''
CREATE TYPE public.warehouse_quantity_type AS (
    warehouse_id integer,
    quantity integer
);


CREATE OR REPLACE FUNCTION public.add_product_with_inventory(p_name text, p_description text, p_price numeric, p_warehouses warehouse_quantity_type[])
 RETURNS TABLE(product_id integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Verificar si el producto ya existe
    IF EXISTS (SELECT 1 FROM products WHERE name = p_name) THEN
        RAISE EXCEPTION 'Ya existe un producto con este nombre.';
    END IF;

    -- Insertar el producto
    INSERT INTO products (name, description, price, creation_date)
    VALUES (p_name, p_description, p_price, now())
    RETURNING id INTO product_id;

    -- Verificar si el producto fue creado
    IF NOT EXISTS (SELECT 1 FROM products WHERE id = product_id) THEN
        RAISE EXCEPTION 'No se pudo crear el producto.';
    END IF;

    -- Verificar si los almacenes existen
    IF EXISTS (
        SELECT 1
        FROM UNNEST(p_warehouses) AS rec
        WHERE NOT EXISTS (SELECT 1 FROM warehouses WHERE id = (rec).warehouse_id)
    ) THEN
        RAISE EXCEPTION 'Al menos uno de los almacenes especificados no existe.';
    END IF;

    -- Insertar en la tabla de inventarios
    INSERT INTO inventory (product_id, warehouse_id, quantity, creation_date)
    SELECT
        product_id,
        (rec).warehouse_id,
        (rec).quantity,
        now()
    FROM UNNEST(p_warehouses) AS rec;

    RETURN QUERY SELECT product_id;
END
$function$
;
'''

create_view = """
CREATE OR REPLACE VIEW public.product_inventory_view AS
SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.description AS product_description,
    p.price AS product_price,
    COALESCE(SUM(i.quantity), 0) AS total_quantity
FROM 
    products p
LEFT JOIN 
    inventory i ON p.id = i.product_id
GROUP BY 
    p.id, p.name, p.description, p.price
ORDER BY 
    p.creation_date DESC;
"""

get_product_cart = """
CREATE OR REPLACE FUNCTION get_inventory_details(inventory_ids integer[])
RETURNS json AS $$
DECLARE
    result json;
    missing_ids integer[];
BEGIN
    -- Obtener los detalles de los inventarios existentes
    SELECT json_agg(row_to_json(t))
    INTO result
    FROM (
        SELECT 
            i.id AS id_inventario,
            p.id AS product_id,
            w.id AS warehouse_id,
            p.name AS product_name,
            p.description AS product_description,
            p.price AS product_price,
            w.name AS warehouse_name
        FROM 
            inventory i
        JOIN 
            products p ON i.product_id = p.id
        JOIN 
            warehouses w ON i.warehouse_id = w.id
        WHERE 
            i.id = ANY(inventory_ids)
    ) t;

    -- Encontrar IDs de inventario que no existen en la tabla
    SELECT ARRAY(
        SELECT unnest(inventory_ids) EXCEPT
        SELECT i.id FROM inventory i
    ) INTO missing_ids;

    -- Verificar si hay IDs faltantes
    IF array_length(missing_ids, 1) > 0 THEN
        -- Devolver JSON que incluya los datos existentes y los IDs no encontrados
        RETURN json_build_object(
            'details', result,
            'missing_ids', missing_ids
        );
    ELSE
        RETURN result;
    END IF;
END;
$$ LANGUAGE plpgsql;

"""