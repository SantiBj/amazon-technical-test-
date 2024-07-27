def format_consult_process_sale(serializer):
    items_sale = serializer.validated_data["items_sale"]
    items_sale_tuples = [(w['inventory_id'], w['quantity']) for w in items_sale]
    items_sale_array = (
        "ARRAY["
        + ", ".join([f"ROW({w[0]}, {w[1]})::public.sale_products_type" for w in items_sale_tuples])
        + "]"
    )

    return f"SELECT * FROM process_sale({items_sale_array})"