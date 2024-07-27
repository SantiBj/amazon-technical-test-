

def format_consult_create(serializer):
    name = serializer.validated_data["name"]
    description = serializer.validated_data["description"]
    price = serializer.validated_data["price"]
    warehouses = serializer.validated_data["warehouses"]

    warehouse_tuples = [(w['warehouse_id'], w['quantity']) for w in warehouses]
    warehouse_array = (
        "ARRAY["
        + ", ".join([f"ROW({w[0]}, {w[1]})::public.warehouse_quantity_type" for w in warehouse_tuples])
        + "]"
    )

    return f"SELECT * FROM add_product_with_inventory('{name}', '{description}', {price}, {warehouse_array})"

def format_get_product_inventory(serializer):
    product_ids = serializer.validated_data["products_ids"]
    ids_tuple = tuple(product_ids)
    ids_list = ",".join(map(str, ids_tuple))
    return f"SELECT get_inventory_details(ARRAY[{ids_list}]::integer[])"