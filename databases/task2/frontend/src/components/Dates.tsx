import React, { useEffect, useState } from 'react'
import { TDate } from './models';
import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:8000/api/",
  });



 function TradingDay({date, handleClick}:TDate) {
    date = new Date(Date.parse(date))
    
    const dateStr = ((date)=>`${date.getFullYear()}-${date.getMonth().toString().padStart(2, "0")}-${date.getDay().toString().padStart(2, "0")}`)
  return (
    <div>
       <li className="page-item">
            <a className="page-link" onClick={()=>handleClick(`http://127.0.0.1:8000/api/get_dynamics/?limit=10&skip=0&start_date=${dateStr(date)}&end_date=${dateStr(date)}`)} href="#">
                {date.toLocaleDateString()}
            </a>
        </li> 
    </div>
    
  )
}
  

export default function Dates({handleSource}) {
  const [dates, setDates] = useState<TDate[]>([])

  useEffect(()=>{
    const apiUrl = 'http://localhost:8000/api/last_trading_dates/?count=10';
    fetch(apiUrl)
      .then((res) => res.json())
      .then((dates) => 
        setDates(dates))
    }, []);

  return (
    <div className='navbar navbar-dark'>
        <ul className="pagination">
        {dates.map((date) => {
            return (
                <TradingDay {...date} handleClick={handleSource}/>
            )
        })}
        </ul>
    </div>
  )
}
