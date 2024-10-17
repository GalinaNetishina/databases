export type TItem = {
    exchange_product_name: string,
    exchange_product_id: string
    delivery_basis_name: string
    delivery_basis_id: string
    delivery_type_id: string
    volume: number
    total: number
    count: number 
    date: Date   
  }

export type TDate = {
  date: Date
}

export type TItemList = {
  items: TItem[]
}
  

