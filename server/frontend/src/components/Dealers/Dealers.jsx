// import React, { useState, useEffect } from 'react';
// import "./Dealers.css";
// import "../assets/style.css";
// import Header from '../Header/Header';
// import review_icon from "../assets/reviewicon.png"

// const Dealers = () => {
//   const [dealersList, setDealersList] = useState([]);
//   // let [state, setState] = useState("")
//   let [states, setStates] = useState([])

//   // let root_url = window.location.origin
//   let dealer_url ="/djangoapp/get_dealers";
  
//   let dealer_url_by_state = "/djangoapp/get_dealers/";
 
//   const filterDealers = async (state) => {
//     dealer_url_by_state = dealer_url_by_state+state;
//     const res = await fetch(dealer_url_by_state, {
//       method: "GET"
//     });
//     const retobj = await res.json();
//     if(retobj.status === 200) {
//       let state_dealers = Array.from(retobj.dealers)
//       setDealersList(state_dealers)
//     }
//   }

//   const get_dealers = async ()=>{
//     const res = await fetch(dealer_url, {
//       method: "GET"
//     });
//     const retobj = await res.json();
//     if(retobj.status === 200) {
//       let all_dealers = Array.from(retobj.dealers)
//       let states = [];
//       all_dealers.forEach((dealer)=>{
//         states.push(dealer.state)
//       });

//       setStates(Array.from(new Set(states)))
//       setDealersList(all_dealers)
//     }
//   }
//   useEffect(() => {
//     get_dealers();
//   },[]);  


// let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;
// return(
//   <div>
//       <Header/>

//      <table className='table'>
//       <tr>
//       <th>ID</th>
//       <th>Dealer Name</th>
//       <th>City</th>
//       <th>Address</th>
//       <th>Zip</th>
//       <th>
//       <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
//       <option value="" selected disabled hidden>State</option>
//       <option value="All">All States</option>
//       {states.map(state => (
//           <option value={state}>{state}</option>
//       ))}
//       </select>        

//       </th>
//       {isLoggedIn ? (
//           <th>Review Dealer</th>
//          ):<></>
//       }
//       </tr>
//      {dealersList.map(dealer => (
//         <tr>
//           <td>{dealer['id']}</td>
//           <td><a href={'/dealer/'+dealer['id']}>{dealer['full_name']}</a></td>
//           <td>{dealer['city']}</td>
//           <td>{dealer['address']}</td>
//           <td>{dealer['zip']}</td>
//           <td>{dealer['state']}</td>
//           {isLoggedIn ? (
//             <td><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review"/></a></td>
//            ):<></>
//           }
//         </tr>
//       ))}
//      </table>;
//   </div>
// )
// }

// export default Dealers

import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const dealer_url ="/api/dealers/";

  const filterDealers = async (state) => {
    const res = await fetch(`/api/dealers/?state=${state}`, {
      method: "GET"
    });
    const data = await res.json();
    if(data.status === 200) {
      setDealersList(data.dealers);
    }
  }

  // const get_dealers = async () => {
  //   const res = await fetch(dealer_url, {
  //     method: "GET"
  //   });
  //   const data = await res.json();
  //   if(data.status === 200) {
  //     const all_dealers = data.dealers;
  //     const uniqueStates = [...new Set(all_dealers.map(dealer => dealer.zip_state))];
  //     setStates(uniqueStates);
  //     setDealersList(all_dealers);
  //   }
  // };


  // const get_dealers = async () => {
//   try {
//     const res = await fetch(dealer_url);
//     const data = await res.json();
//     console.log("Data received in get_dealers:", data);

//     if (Array.isArray(data)) {
//       const all_dealers = data;
//       const uniqueStates = [...new Set(all_dealers.map(dealer => dealer.zip_state))];
//       setStates(uniqueStates);
//       setDealersList(all_dealers);
//     } else {
//       console.error("Unexpected data format:", data);
//     }
//   } catch (error) {
//     console.error("Fetch failed:", error);
//   }
// };

  // const get_dealers = async () => {
  //   const res = await fetch(dealer_url);
  //   const data = await res.json();
  //   console.log("Data received in get_dealers:", data); // This is now the array

  //   if (Array.isArray(data)) { // Check if data is an array
  //     setDealersList(data);
  //     const uniqueStates = [...new Set(data.map(dealer => dealer.zip_state))];
  //     setStates(uniqueStates);
  //   } else {
  //     console.error("Error fetching dealers: Expected an array but received:", data);
  //   }
  // };

  // Update your code to match the actual structure of the response. If your backend just returns an array of dealers directly, the fix is:
  const get_dealers = async () => {
  const res = await fetch(dealer_url);
  const data = await res.json();
  console.log("Data received in get_dealers:", data); // Inspect the data
  if(data && data.status === 200 && data.dealers) {
    const all_dealers = data.dealers;
    const uniqueStates = [...new Set(all_dealers.map(dealer => dealer.zip_state))];
    setStates(uniqueStates);
    setDealersList(all_dealers);
  } else {
    console.error("Error fetching or processing dealers:", data);
    }
  };
  useEffect(() => {
    get_dealers();
  },[]);

  let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;
  return(
    <div>
      <Header/>

     <table className='table'>
      <thead>
        <tr>
          <th>ID</th>
          <th>Dealer Name</th>
          <th>City</th>
          <th>Address</th>
          <th>Zip</th>
          <th>
            <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
              <option value="" disabled selected hidden>State</option>
              <option value="All">All States</option>
              {states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </th>
          {isLoggedIn ? (
            <th>Review Dealer</th>
          ) : null}
        </tr>
      </thead>
      <tbody>
        {dealersList.map(dealer => (
          <tr key={dealer.id}>
            <td>{dealer.id}</td>
            <td><a href={`/dealer/${dealer.id}`}>{dealer.name}</a></td>
            <td>{dealer.city}</td>
            <td>{dealer.address}</td>
            <td>{dealer.zip_state}</td>
            <td>{dealer.zip_state}</td>
            {isLoggedIn ? (
              <td><a href={`/postreview/${dealer.id}`}><img src={review_icon} className="review_icon" alt="Post Review"/></a></td>
            ) : null}
          </tr>
        ))}
      </tbody>
     </table>
    </div>
  )
}

export default Dealers;