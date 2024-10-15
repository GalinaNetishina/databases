export type TItem = {
    exchange_product_name: string,
    exchange_product_id: string
    delivery_basis_name: string
    volume: number
    total: number
    count: number 
    date: Date   
  }

export type TItemList = {
  items: TItem[]
}
  

