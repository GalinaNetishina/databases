import { TItem, TItemList } from "./models";

function Item({
  exchange_product_id,
   exchange_product_name,
  delivery_basis_name,
total, count, volume}: TItem) {
  return (
    <tr className="line">      
      <td className="number">{exchange_product_id}</td>
      <td>{exchange_product_name}</td>
      <td>{delivery_basis_name}</td>
      <td className="number">{count}</td>
      <td className="number">{volume}</td>
      <td className="number">{total}</td> 
    </tr>)
}

export default function ListView({items}: TItemList) {
  return (
    <div>
      {items.map((item: TItem) =>
        <Item {...item} />)}      
    </div>
  )
}