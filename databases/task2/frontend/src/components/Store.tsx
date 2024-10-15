import { useState, useEffect } from 'react';
import ListView from './ListView.tsx';
import { TItem } from './models.tsx';


export default function Store () {
  const [items, setItems] = useState<TItem[]>([])

  useEffect(() => {
    const apiUrl = 'http://localhost:8000/get_trading_results/';
    fetch(apiUrl)
      .then((res) => res.json())
      .then((items) => 
        setItems(items))
      }, []);


  return (
    <div>
      <h1>Trading Results</h1>
      <ListView items={items} />
    </div>
  )
    
}
