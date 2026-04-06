await callback_query.message.edit_text(
    text,
    reply_markup=await inline.build_pagination_keyboard(
        items=list_of_specs,  # Здесь должен быть отфильтрованный список
        page=0,
        item_type="spec_card",  # Новый тип для пагинации внутри карточки
        items_per_page=5
    )
)

elif item_type == "spec":
# Выбрали специальность -> показываем вузы
text = f"Вузы со специальностью ID {item_id}:"

await callback_query.message.edit_text(
    text,
    reply_markup=await inline.build_pagination_keyboard(
        items=list_of_unis,
        page=0,
        item_type="uni_card",
        items_per_page=1
    )
)

await callback_query.answer()